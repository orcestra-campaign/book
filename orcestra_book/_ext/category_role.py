#!/usr/bin/env python3
from docutils import nodes

from sphinx.util.docutils import SphinxRole


class CategoryRole(SphinxRole):
    def run(self):
        tier = {
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
        }.get(self.text, "unknown")

        node = nodes.raw(
            text=f'<span class="badge cat-{tier} cat-{self.text}">{self.text}</span>',
            format="html",
        )

        return [node], []


def setup(app):
    app.add_role("cat", CategoryRole())

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
