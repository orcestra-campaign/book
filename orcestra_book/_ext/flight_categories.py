import pathlib
from docutils import nodes
from functools import lru_cache

import yaml
from sphinx.util.docutils import SphinxRole, SphinxDirective
from orcestra.utils import load_frontmatter


def get_flight_categories(src):
    with open(src / "operation" / "flight_categories.yaml", "r") as fp:
        return yaml.safe_load(fp)["categories"]


@lru_cache
def create_flight_badge(src, cat_id):
    """Return an HTML node based on a flight category id."""
    categories = get_flight_categories(src)
    cat_tier = {
        key: attrs["tier"]
        for key, attrs in categories.items()
    }.get(cat_id, "unknown")

    span = f'<span class="badge cat-{cat_tier} cat-{cat_id}">{cat_id}</span>'
    href = f'<a href="https://orcestra-campaign.org/search.html?q={cat_id}">{span}</a>'
    node = nodes.raw(
        text=href,
        format="html",
    )

    return node


class FlightCategoryRole(SphinxRole):
    """Create a badge based on a given flight category."""

    def run(self):
        src = pathlib.Path(self.env.srcdir)
        node = create_flight_badge(src, self.text)

        return [node], []


class CategoryDirective(SphinxDirective):
    """Create a table of all defined flight categories."""
    def run(self):
        src = pathlib.Path(self.env.srcdir)
        categories = get_flight_categories(src)

        table_dict = dict(
            ID=[create_flight_badge(src, k) for k in categories],
            Description=[d["long_name"] for d in categories.values()],
            Tier=[nodes.strong(text=d["tier"].upper()) for d in categories.values()],
        )

        # create table with correct number of columns
        table = nodes.table()
        tgroup = nodes.tgroup(cols=len(table_dict))
        table += tgroup

        # Set column width based on expected content (IDs and tiers are short)
        for col_id in table_dict:
            tgroup += nodes.colspec(colwidth=0.5 if col_id in ("ID", "Tier") else 1)

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
                if isinstance(table_dict[key][i], nodes.Node):
                    row += nodes.entry("", table_dict[key][i])
                else:
                    row += nodes.entry("", nodes.paragraph(text=table_dict[key][i]))
            tbody += row

        return [table]


class BadgesDirective(SphinxDirective):
    """Create a list of badges based on all categories defined in YAML front matter."""

    def run(self):
        src = pathlib.Path(self.env.srcdir)
        fm = load_frontmatter(self.env.doc2path(self.env.docname))
        categories = fm.get("categories", [])

        node_list = [create_flight_badge(src, cat_id) for cat_id in categories]

        node = nodes.raw(
            text=" ".join(n.astext() for n in node_list),
            format="html",
        )

        return [node]


def setup(app):
    app.add_role("flight-cat", FlightCategoryRole())
    app.add_directive("badges", BadgesDirective)
    app.add_directive("categories", CategoryDirective)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
