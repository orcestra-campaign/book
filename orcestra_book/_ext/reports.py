#!/usr/bin/env python3
import os
import pathlib
import subprocess
from datetime import datetime
from docutils import nodes
from functools import lru_cache, partial

import yaml
from jinja2 import Template
from sphinx.util.docutils import SphinxRole


@lru_cache
def load_frontmatter(path, derive_flight=False):
    with open(path, "r") as fp:
        frontmatter = next(yaml.safe_load_all(fp))

    if derive_flight:
        takeoff = frontmatter["takeoff"]
        landing = frontmatter["landing"]

        frontmatter["expr_date"] = takeoff.strftime("%d %B %Y")
        frontmatter["expr_takeoff"] = takeoff.strftime("%X")
        frontmatter["expr_landing"] = landing.strftime("%X")
        frontmatter["expr_categories"] = map(
            lambda s: f"{{flight-cat}}`{s}`", frontmatter.get("categories", [])
        )

    return frontmatter


@lru_cache
def create_flight_badge(src, cat_id):
    """Return an HTML node based on a flight category id."""
    with open(src / "reports" / "flight_categories.yaml", "r") as fp:
        cat_tier = {
            key: attrs["tier"]
            for key, attrs in yaml.safe_load(fp)["categories"].items()
        }.get(cat_id, "unknown")

    span = f'<span class="badge cat-{cat_tier} cat-{cat_id}">{cat_id}</span>'
    href = f'<a href="https://orcestra-campaign.org/search.html?q={cat_id}">{span}</a>'
    node = nodes.raw(
        text=href,
        format="html",
    )

    return node


class FlightCategoryRole(SphinxRole):
    def run(self):
        src = pathlib.Path(self.env.srcdir)
        node = create_flight_badge(src, self.text)

        return [node], []


class BadgesRole(SphinxRole):
    def run(self):
        src = pathlib.Path(self.env.srcdir)
        fm = load_frontmatter(self.env.doc2path(self.env.docname))
        categories = fm.get("categories", [])

        node_list = [create_flight_badge(src, cat_id) for cat_id in categories]

        node = nodes.raw(
            text=" ".join(n.astext() for n in node_list),
            format="html",
        )

        return [node], []


class LogoRole(SphinxRole):
    """Add a small campaign logo to the upper-right corner of a page."""
    def run(self):
        src = pathlib.Path(self.env.srcdir)

        logo_path = list((src / "logos").glob(f"*_{self.text}.svg"))
        doc_path = pathlib.Path(self.env.doc2path(self.env.docname))

        if len(logo_path) == 0:
            raise Exception(f"No logo found for {self.text}")
        else:
            rel_path = logo_path[0].relative_to(doc_path.parent, walk_up=True)

            node = nodes.image(uri=rel_path.as_posix(), alt=f"{self.text} logo")
            node['classes'].append('campaign-logo')  # Ad

        return [node], []


def collect_halo_refs(src, flight_id):
    refs =  ", ".join(
        f"[{t}](../{t}s/{flight_id})" for t in ("plan", "report")
        if (src / f"{t}s" / f"{flight_id}.md").is_file()
    )

    return f"{flight_id} ({refs})"


def write_flight_table(app):
    src = pathlib.Path(app.srcdir)
    flights = (src / "reports").glob("HALO-[0-9]*[a-z].md")

    func = partial(load_frontmatter, derive_flight=True)
    frontmatters = {fm["flight_id"]: fm for fm in map(func, sorted(flights))}

    for flight_id in frontmatters:
        frontmatters[flight_id]["expr_refs"] = collect_halo_refs(src, flight_id)

    with open(src / "_templates" / "operation_halo.md", "r") as fp:
        templ = fp.read()

    with open(src / "operation" / "halo.md", "w") as fp:
        t = Template(templ)
        fp.write(t.render(flights=frontmatters))


def write_ship_table(app):
    src = pathlib.Path(app.srcdir)
    reports = (src / "reports").glob("METEOR-[0-9]*.md")

    frontmatters = {fm["report_id"]: fm for fm in map(load_frontmatter, sorted(reports))}

    with open(src / "_templates" / "operation_rvmeteor.md", "r") as fp:
        templ = fp.read()

    with open(src / "operation" / "rvmeteor.md", "w") as fp:
        t = Template(templ)
        fp.write(t.render(reports=frontmatters))


def setup(app):
    app.connect("builder-inited", write_flight_table)
    app.connect("builder-inited", write_ship_table)

    app.add_role("flight-cat", FlightCategoryRole())
    app.add_role("badges", BadgesRole())
    app.add_role("logo", LogoRole())

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
