from docutils import nodes
from functools import lru_cache

import yaml
from sphinx.util.docutils import SphinxRole


@lru_cache
def load_frontmatter(path):
    """Load and return the front matter section of a YAML file."""
    with open(path, "r") as fp:
        frontmatter = next(yaml.safe_load_all(fp))

    return frontmatter


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
