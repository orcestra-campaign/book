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
            lambda s: f"{{cat}}`{s}`", frontmatter.get("categories", [])
        )

    return frontmatter


@lru_cache
def create_badge(cat_id):
    """Return an HTML node based on a category id."""
    with open("orcestra_book/flight_reports/categories.yaml", "r") as fp:
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


class CategoryRole(SphinxRole):
    def run(self):
        node = create_badge(self.text)

        return [node], []


class BadgesRole(SphinxRole):
    def run(self):
        fm = load_frontmatter(self.env.doc2path(self.env.docname))
        categories = fm.get("categories", [])

        node_list = [create_badge(cat_id) for cat_id in categories]

        node = nodes.raw(
            text=" ".join(n.astext() for n in node_list),
            format="html",
        )

        return [node], []


class FrontmatterRole(SphinxRole):
    def run(self):
        """Access variables defined in document front matter."""
        fm = load_frontmatter(self.env.doc2path(self.env.docname))

        return nodes.raw(text=fm[self.text]), []


def collect_fronmatter():
    flights = pathlib.Path("orcestra_book/flight_reports/").glob("*[0-9]*[a-z].md")
    func = partial(load_frontmatter, derive_flight=True)

    return {fm["flight_id"]: fm for fm in map(func, sorted(flights))}


def write_flight_table(app):
    frontmatters = collect_fronmatter()

    with open("orcestra_book/_templates/operation.md", "r") as fp:
        templ = fp.read()

    with open("orcestra_book/operation.md", "w") as fp:
        t = Template(templ)
        fp.write(t.render(flights=frontmatters))


def setup(app):
    app.connect("builder-inited", write_flight_table)

    app.add_role("cat", CategoryRole())
    app.add_role("badges", BadgesRole())
    app.add_role("front", FrontmatterRole())

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
