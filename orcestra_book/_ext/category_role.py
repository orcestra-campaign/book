#!/usr/bin/env python3
from docutils import nodes

import yaml
from frontmatter import Frontmatter
from sphinx.util.docutils import SphinxRole


def create_badge(cat_id):
    """Return an HTML node based on a category id."""
    with open("orcestra_book/flight_reports/categories.yaml", "r") as fp:
        cat_tier = {
            key: attrs["tier"] for key, attrs in yaml.safe_load(fp)["categories"].items()
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
        """(Re-)parse the frontmatter of the current document and create badges."""
        categories = Frontmatter.read_file(
            self.env.doc2path(self.env.docname)
        )["attributes"].get("categories", [])

        nodes = [create_badge(cat_id) for cat_id in categories]

        return nodes, []


def setup(app):
    app.add_role("cat", CategoryRole())
    app.add_role("badges", BadgesRole())

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
