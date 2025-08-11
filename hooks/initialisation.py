from huggingface_hub import snapshot_download
import dotenv
import os
import logging
from mkdocs.utils.templates import TemplateContext
from mkdocs.structure.pages import Page
from jinja2 import Environment, FileSystemLoader
import glob
import random

from evidence_seeker import (
    EvidenceSeekerResult,
    result_as_markdown,
)
log = logging.getLogger("mkdocs")

SHOW_DETAILS = True


def on_startup(command, dirty):
    results = load_results()
    for ev_result in results:
        construct_result_site(ev_result=ev_result)
    write_index(results=results)


def construct_result_site(ev_result: EvidenceSeekerResult):
    env = Environment(loader=FileSystemLoader("./templates"))
    md_template = env.get_template("result.tmpl")
    translation = {
        "strongly_confirmed": "im hohen Maße bestätigt",
        "confirmed": "bestätigt",
        "weakly_confirmed": "im geringen Maße bestätigt",
        "strongly_disconfirmed": "im hohen Maße widerlegt",
        "disconfirmed": "widerlegt",
        "weakly_disconfirmed": "im geringen Maße widerlegt",
        "inconclusive_confirmation": "weder bestätigt noch widerlegt",
        "ascriptive": "zuschreibend",
        "descriptive": "deskriptiv",
        "normative": "normativ",
    }
    md = result_as_markdown(
        ev_result,
        translation,
        md_template,
        group_docs_by_sources=True
    )
    with open(
        f"./docs/results/{ev_result.uid}.md",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(md)


def write_index(results: list[EvidenceSeekerResult]):
    global SHOW_DETAILS
    _results = [
        {
            "statement": res.request,
            "count_claims": res.count_claims(),
            "time": res.time,
            "feedback": res.feedback["binary"],
            "uid": res.uid,
        }
        for res in results
    ]
    random.shuffle(_results)
    env = Environment(loader=FileSystemLoader("./templates"))
    md_template = env.get_template("index.tmpl")
    with open("./docs/index.md", "w", encoding="utf-8") as f:
        md = md_template.render(_results=_results, show_details=SHOW_DETAILS)
        f.write(md)


def load_results():
    results = []
    for p in glob.glob(
        pathname="**/*.yaml", root_dir="./data/", recursive=True
    ):
        results.append(EvidenceSeekerResult.from_logfile("./data/" + p))
    return results


def on_page_context(
    context: TemplateContext, page: Page, config, nav
) -> TemplateContext | None:
    log.info(f"---- {page.title} ----")
    log.info(f"Meta: {page.meta}, {page.url}, {page.file.src_path}")
    return context
