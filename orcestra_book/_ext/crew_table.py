from functools import lru_cache

import yaml

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective
from orcestra.utils import load_frontmatter


class CrewTableDirective(SphinxDirective):
    option_spec = {
        "columns": lambda arg: [item.strip() for item in arg.split(",")],
    }

    def run(self):
        """Add crew member table."""
        # Access variables defined in document front matter.
        columns = self.options.get("columns", ["job", "name"])
        fm = load_frontmatter(self.env.doc2path(self.env.docname))
        crew = fm["crew"]
        table_dict = {
            key.capitalize(): [item.get(key, "---") for item in crew] for key in columns
        }

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


class CrewListDirective(SphinxDirective):
    def run(self):
        """Add crew member list."""
        fm = load_frontmatter(self.env.doc2path(self.env.docname))

        return [nodes.inline(text=", ".join(m["name"] for m in fm["crew"]))]


class InstrumentTableDirective(SphinxDirective):
    option_spec = {
        "columns": lambda arg: [item.strip() for item in arg.split(",")],
    }

    def run(self):
        """Add crew member table."""
        # Access variables defined in document front matter.
        columns = self.options.get("columns", ["operational", "comment"])
        fm = load_frontmatter(self.env.doc2path(self.env.docname))

        instruments = fm["instruments"]
        table_dict = {"Instrument": list(instruments.keys())}
        table_dict.update(
            {
                key.capitalize(): [i.get(key, "---") for i in instruments.values()]
                for key in columns
            }
        )

        if "Operational" in table_dict:
            table_dict["Operational"] = ["\u2705" if status else "\u274c" for status in table_dict["Operational"]]

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
    app.add_directive("crew-list", CrewListDirective)
    app.add_directive("instrument-table", InstrumentTableDirective)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
