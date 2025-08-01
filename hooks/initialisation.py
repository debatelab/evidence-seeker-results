from huggingface_hub import snapshot_download
import dotenv
import os
import logging
from mkdocs.utils.templates import TemplateContext
from mkdocs.structure.pages import Page
from jinja2 import Environment, FileSystemLoader
import glob
import random

from evidence_seeker.results import EvidenceSeekerResult

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
    snapshot_download(repo_id="DebateLabKIT/evidence-seeker-appdata", local_files_only=True, repo_type="dataset", allow_patterns="*.yaml", local_dir="./data", token=os.environ["HF_TOKEN"])

def on_startup(command, dirty):
    #download()
    results = load_results()
    for ev_result in results:
        construct_result_site(ev_result=ev_result)
    write_index(results=results)

def construct_result_site(ev_result : EvidenceSeekerResult):
    env = Environment(loader=FileSystemLoader("./templates"))
    md_template = env.get_template("result.tmpl")
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
    env = Environment(loader=FileSystemLoader("./templates"))
    md_template = env.get_template("index.tmpl")
    with open("./docs/index.md", "w", encoding="utf-8") as f:
        md = md_template.render(_results=_results, show_details=True)
        f.write(md)

def load_results():
    results = []
    for p in glob.glob(pathname="**/request_*.yaml", root_dir="./data/", recursive=True):
        results.append(EvidenceSeekerResult.from_logfile("./data/" + p))
    return results

def on_page_context(context : TemplateContext, page : Page, config, nav) -> TemplateContext | None:
    log.info(f"---- {page.title} ----")
    log.info(f"Meta: {page.meta}, {page.url}, {page.file.src_path}")
    return context
