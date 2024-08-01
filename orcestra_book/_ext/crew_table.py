from functools import lru_cache

import yaml

from docutils import nodes
from sphinx.util.docutils import SphinxDirective


@lru_cache
def load_frontmatter(path):
    """Load and return the front matter section of a YAML file."""
    with open(path, "r") as fp:
        frontmatter = next(yaml.safe_load_all(fp))

    return frontmatter


class CrewTableDirective(SphinxDirective):
    def run(self):
        """Add crew member table."""
        # Access variables defined in document front matter.

        fm = load_frontmatter(self.env.doc2path(self.env.docname))
        crew = fm["crew"]
        table_dict = dict(
            Name=[list(item.values())[0] for item in crew],
            Job=[list(item.values())[1] for item in crew],
        )

        # create table with correct number of columns
        table = nodes.table()
        tgroup = nodes.tgroup(cols=len(table_dict))
        table += tgroup

        for _ in table_dict:
            tgroup += nodes.colspec(colwidth=1)

        # Create header
        thead = nodes.thead()
        tgroup += thead
        header_row = nodes.row()
        for key in table_dict.keys():
            header_row += nodes.entry("", nodes.paragraph(text=key))
        thead += header_row

        # Create table body
        tbody = nodes.tbody()
        tgroup += tbody
        num_rows = len(list(table_dict.values())[0])
        for i in range(num_rows):
            row = nodes.row()
            for key in table_dict.keys():
                row += nodes.entry("", nodes.paragraph(text=table_dict[key][i]))
            tbody += row

        return [table]


def setup(app):
    app.add_directive("crew", CrewTableDirective)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
