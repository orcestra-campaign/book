from docutils import nodes
from functools import lru_cache

import yaml
from sphinx.util.docutils import SphinxRole
from orcestra.utils import load_frontmatter


class FrontmatterRole(SphinxRole):
    def run(self):
        """Access variables defined in document front matter."""
        fm = load_frontmatter(self.env.doc2path(self.env.docname))

        return nodes.raw(text=fm[self.text]), []


def setup(app):
    app.add_role("front", FrontmatterRole())

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
