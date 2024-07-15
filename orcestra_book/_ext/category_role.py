#!/usr/bin/env python3
from docutils import nodes

from frontmatter import Frontmatter
from sphinx.util.docutils import SphinxRole


def create_badge(cat_id):
    """Return an HTML node based on a category id."""
    cat_tier = {
       # Important objectives
       "ec_under": "a",
       "ec_track": "a",
       "two_circ": "a",
       "itcz_circ": "a",
       # Semi-important objectives
       "south": "b",
       "atr_circ": "b",
       "atr_over": "b",
       "sar": "b",
       "pace": "b",
       "gpm": "b",
       "mindels": "b",
       "cloud_circ": "b",
       "curtain": "b",
       "radar": "b",
       # Nice-to-have
       "cirrus": "c",
    }.get(cat_id, "unknown")

    node = nodes.raw(
        text=f'<span class="badge cat-{cat_tier} cat-{cat_id}">{cat_id}</span>',
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
