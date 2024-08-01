import pathlib
from docutils import nodes
from functools import lru_cache

import yaml
from sphinx.util.docutils import SphinxRole, SphinxDirective


@lru_cache
def load_frontmatter(path):
    """Load and return the front matter section of a YAML file."""
    with open(path, "r") as fp:
        frontmatter = next(yaml.safe_load_all(fp))

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
    """Create a badge based on a given flight category."""

    def run(self):
        src = pathlib.Path(self.env.srcdir)
        node = create_flight_badge(src, self.text)

        return [node], []


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

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
