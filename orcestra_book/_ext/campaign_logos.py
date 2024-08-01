import pathlib
from docutils import nodes

from sphinx.util.docutils import SphinxRole


class LogoRole(SphinxRole):
    """Add a small campaign logo to the upper-right corner of a page."""

    def run(self):
        src = pathlib.Path(self.env.srcdir)

        logo_path = list((src / "logos").glob(f"*_{self.text}.svg"))
        doc_path = pathlib.Path(self.env.doc2path(self.env.docname))

        if len(logo_path) == 0:
            raise Exception(f"No logo found for {self.text}")
        else:
            rel_path = logo_path[0].relative_to(doc_path.parent, walk_up=True)

            node = nodes.image(uri=rel_path.as_posix(), alt=f"{self.text} logo")
            node["classes"].append("campaign-logo")

        return [node], []


def setup(app):
    app.add_role("logo", LogoRole())

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
