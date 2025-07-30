from huggingface_hub import snapshot_download
import dotenv
import os
import logging
from mkdocs.utils.templates import TemplateContext
from mkdocs.structure.pages import Page
from jinja2 import Environment
import glob
import random

from evidence_seeker.results import EvidenceSeekerResult

overview_template = """
# Ergebnisse der EvidenceSeeker-DemoApp

Die EvidenceSeeker-Pipeline ist ein RAG-basierter LLM-Workflow für das Fact-Checking beliebiger Aussagen relativ zu einer gegebenen Datenbasis. Die EvidenceSeeker-Pipeline wurde im Rahmen des [KIdeKu-Projekts](https://compphil2mmae.github.io/research/kideku/) am Karlsruher Institut für Technologie entwickelt. KIdeKu wird gefördert vom [BMFSFJ](https://www.bmbfsfj.bund.de/).

Diese Webseite sammelt Ergebnisse der Pipeline, die durch Nutzer*inneninteraktion über eine DemoApp erstellt wurden. Die der DemoApp zugrundeliegende Datenbasis verwendet die Artikel des Jahrgangs 2024 der Zeitschrift [APuZ](https://www.bpb.de/shop/zeitschriften/apuz/), die von der Bundeszentrale für politische Bildung herausgegeben wird.

[:simple-huggingface: DemoApp jetzt selbst ausprobieren](https://huggingface.co/spaces/DebateLabKIT evidence-seeker-demo){ .md-button .md-button--primary }
### Beispiele

!!! warning "Inhaltswarnung"

    Die folgenden Beispiele enthalten reale Nutzer\\*inneneingaben, die auf ihre Inhalte von den Ersteller\\*innen dieser Seite nicht geprüft wurden 
    und möglicherweise sensible oder für manche Personen beunruhigende Inhalte haben können. 
    Die beinhalteten Aussagen und ihre Bewertung durch die Pipeline geben nicht die Meinung der Ersteller\\*innen dieser Seite wieder.

<div class="grid cards" markdown>

{% for ev_result in _results %}
-   :fontawesome-solid-quote-right:  _{{ ev_result.statement }}_

    ---

    Analysiert als

    - {{ ev_result.count_claims["ascriptive"] }} askriptive,
    - {{ ev_result.count_claims["normative"] }} normative
    - und {{ ev_result.count_claims["descriptive"] }} deskriptive Aussagen

    ---
    {% if ev_result.feedback == 'positive' %}
    :material-thumb-up-outline:{ .lg .top .thumbup } <font color="grey" size=size=2em>{{ ev_result.time }}</font>
    {% elif ev_result.feedback == 'negative' %}
    :material-thumb-down-outline:{ .lg .top .thumbdown } <font color="grey" size=size=2em>{{ ev_result.time }}</font>
    {% else %}
    :material-dots-circle:{ .lg .top } <font color="grey" size=size=2em>{{ ev_result.time }}</font>
    {% endif %}

    [:octicons-arrow-right-24: Details](results/result_{{ ev_result.request_uid }})

{% endfor %}
</div>
"""

result_template = """
# Ergebnis der EvidenceSeeker-Pipeline

## Originale Eingabe

!!! quote "<font size="4pt" color="rgb(31, 31, 31)">*{{ statement }}*</font>"

    <div style="text-align: right;" markdown><font color="grey">{{ time }}</font></div>

## Ergebnisse

Es folgen die von der Pipeline gefundene Präzisierungen der eingegebenen Aussagen und deren Bewertung bezüglich der gegebenen Datenbasis.

{% for claim, sources in claims %}
---

**Präzisierte Aussage:** _{{ claim.text }}_ <font color="orange">[{{ translation[claim.statement_type.value] }}e Aussage]</font>

**Status**: {{ translation[claim.verbalized_confirmation] }}

{% if sources is not none %}

|Metrik|Wert|
|:---|---:|
|Durchschnittliche Bestätigung|{{ "%.3f"|format(claim.average_confirmation) }} |
|Evidentielle Abweichung|{{ "%.3f"|format(claim.evidential_uncertainty) }}|
|Breite der Evidenzbasis|{{ "%.3f"|format(claim.n_evidence) }}|

{{ sources }}
{% else %}
Aussagen vom Typ '{{ translation[claim.statement_type.value] }}' wurden vom EvidenceSeeker nicht geprüft.
{% endif %}
{% endfor %}

## Feedback des\\*der Nutzer\\*in

Bewertung der Ergebnisse durch den\\*die Nutzer\\*in

{% if feedback == 'positive' %}
<div class="grid cards" style="background-color:rgb(153, 205, 50, 0.15)" markdown>
- :material-thumb-up-outline:{ .lg .top .thumbup } 
    Der\\*die originale Nutzer\\*in hat die Ergebnisse der EvidenceSeeker-Pipeline <font color="yellowgreen">**positiv**</font> bewertet.
</div>
{% elif feedback == 'negative' %}
<div class="grid cards" style="background-color:rgb(255, 99, 71, 0.15)" markdown>
- :material-thumb-down-outline:{ .lg .top .thumbdown } 
    Der\\*die originale Nutzer\\*in hat die Ergebnisse der EvidenceSeeker-Pipeline <font color="tomato">**negativ**</font> bewertet.
</div>
{% else %}
<div class="grid cards" style="background-color:rgb(211, 211, 211, 0.15)" markdown>
- :material-dots-circle:{ .lg .top .neutral } 
    Der\\*die originale Nutzer\\*in hat die Ergebnisse der EvidenceSeeker-Pipeline nicht bewertet.
</div>
{% endif %}
"""

log = logging.getLogger('mkdocs')

def get_sources(documents, confirmation_by_document) -> str | None:
    grouped = {}
    for doc in documents:
        if doc["metadata"]["file_name"] not in grouped.keys():
            grouped[doc["metadata"]["file_name"]] = {"author": doc["metadata"]["author"],
                                                    "url": doc["metadata"]["url"],
                                                    "title": doc["metadata"]["title"].replace("{","").replace("}",""),
                                                    "texts": [{"original_text": doc["metadata"]["original_text"], 
                                                               "conf": confirmation_by_document[doc["uid"]],
                                                               "full_text": doc["text"]}]}
        else:
            grouped[doc["metadata"]["file_name"]]["texts"].append({"original_text": doc["metadata"]["original_text"], "conf": confirmation_by_document[doc["uid"]], "full_text": doc["text"]})

    t = []
    for doc in grouped.keys():
        grouped[doc]["texts"] = sorted(grouped[doc]["texts"], key=lambda item: item["conf"], reverse=True)
        t.append(f"    {grouped[doc]['author']}: *{grouped[doc]['title']}* ([Link]({grouped[doc]['url']})):")
        for text in grouped[doc]["texts"]:
            orig = text["original_text"].strip().replace("\n"," ").replace('"',"'")
            short = f'"{orig}" **[{round(text["conf"],5)}]**'
            detailed = '"' + text["full_text"].strip().replace("\n","").replace('"',"'") + '"'
            part = f"    - {short}\n"
            part += f"        <details>\n"
            part += f"        <summary>Mehr Details</summary>\n"
            part += f"        {detailed}\n"
            part += f"        </details>"
            t.append(part)
    if len(t) == 0:
        return None
    else:
        t = "\n\n".join(t) + "\n\n"
        return '\n\n??? abstract "Verwendete Quellen"\n\n' + t + '\n\n'

def download():
    dotenv.load_dotenv()
    assert "HF_TOKEN" in os.environ.keys()
    snapshot_download(repo_id="DebateLabKIT/evidence-seeker-appdata", local_files_only=True, repo_type="dataset", allow_patterns="*.yaml", local_dir="./res/", token=os.environ["HF_TOKEN"])

def on_startup(command, dirty):
    #download()
    results = load_results()
    for ev_result in results:
        construct_result_site(ev_result=ev_result)
    write_index(results=results)

def construct_result_site(ev_result : EvidenceSeekerResult):
    env = Environment()
    md_template = env.from_string(result_template)
    claims = [(claim, get_sources(claim["documents"], claim["confirmation_by_document"])) for claim in ev_result.claims]
    translation = {
        "ascriptive": "askriptiv",
        "descriptive": "deskriptiv",
        "normative": "normativ",
        "The claim is neither confirmed nor disconfirmed.": "Die Aussage wird weder bestätigt noch widerlegt.",
        "The claim is strongly confirmed.": "Die Aussage wird im hohen Maße bestätigt.",
        "The claim is strongly disconfirmed.": "Die Aussage wird im hohen Maße widerlegt.",
        "The claim is weakly confirmed.": "Die Aussage wird in geringem Maße bestätigt.",
        "The claim is weakly disconfirmed.": "Die Aussage wird in geringem Maße widerlegt."
    }
    md = md_template.render(
        feedback=ev_result.feedback["binary"],
        statement=ev_result.request,
        time=ev_result.request_time,
        claims=claims,
        translation=translation
    )
    meta = f"---\ntitle: Beispielausgabe ({ev_result.request_time})\ndate: {ev_result.request_time}\n---\n"
    md = meta + md
    with open(f"./docs/results/result_{ev_result.request_uid}.md", "w", encoding="utf-8") as f:
        f.write(md)

def write_index(results : list[EvidenceSeekerResult]):
    _results = [{"statement": res.request, "count_claims": res.count_claims(),"time": res.request_time, "feedback": res.feedback["binary"], "request_uid": res.request_uid} for res in results]
    random.shuffle(_results)
    env = Environment()
    md_template = env.from_string(overview_template)
    with open(f"./docs/index.md", "w", encoding="utf-8") as f:
        md = md_template.render(_results=_results)
        f.write(md)

def load_results():
    results = []
    for p in glob.glob(pathname="request_*.yaml", root_dir="./res"):
        results.append(EvidenceSeekerResult.from_logfile("./res/" + p))
    return results

def on_page_context(context : TemplateContext, page : Page, config, nav) -> TemplateContext | None:
    log.info(f"---- {page.title} ----")
    log.info(f"Meta: {page.meta}, {page.url}, {page.file.src_path}")
    return context
