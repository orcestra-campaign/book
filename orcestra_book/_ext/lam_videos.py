import pathlib
from datetime import datetime, timedelta

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective


SWIFT_CONTAINER = (
    "https://swift.dkrz.de/v1/dkrz_f765c92765f44c068725c0d08cc1e6c5/LAM-ORCESTRA"
)

VARINFO = {
    "cllvi": "Cloud liquid path",
    "clisvi": "Ice and snow water path",
    "prw": "Precipitable water",
    "pr": "Precipitation flux",
    "rsut": "Outgoing shortwave radiation",
    "rlut": "Outgoing longwave radiation",
    "cresfc": "Cloud radiative effect (surface)",
    "cretoa": "Cloud radiative effect (TOA)",
    "hsws": "Surface wind speed",
    "uas": "Zonal wind speed",
    "vas": "Meridional wind speed",
    "sconv": "Surface wind convergence",
    "all-in-one": "All contours at once",
}


def get_source(dt_object, varname, zoom=2, base_url=SWIFT_CONTAINER):
    day = timedelta(days=1)
    simulation_period = f"{dt_object:%m%d}-{dt_object + day:%m%d}"
    return f"{base_url}/{dt_object:%m%d}/zoom-level-{zoom}/{varname}_{simulation_period}_ZoomLvl{zoom}.mp4"


def get_video_node(source_url, width=720):
    source = f"<source src={source_url}>"
    poster = source_url.replace(".mp4", ".png")
    err = "Your browser does not support the video tag."
    video = f"<video width='{width}' controls poster={poster}>  {source} type='mp4'/>{err}</video>"

    raw_node = nodes.raw(
        rawsource="",
        text=video,
        format="html",
    )

    return raw_node


def get_link_node(source_url, message):
    text = nodes.Text(message)
    return nodes.reference("", text, refuri=source_url)


class LimitedAreaVideos(SphinxDirective):
    option_spec = {
        "date": str,
        "variables": lambda arg: [item.strip() for item in arg.split(",")],
        "width": int,
    }

    def run(self):
        dt_object = datetime.fromisoformat(self.options.get("date"))
        variables = self.options.get("variables", VARINFO.keys())
        width = self.options.get("width", 720)

        node_list = []
        for varname in variables:
            src = get_source(dt_object, varname, zoom=1)

            title_node = nodes.title(text=VARINFO.get(varname, varname))
            section_node = nodes.section()
            section_node["ids"] = [varname]
            section_node += title_node
            section_node += get_video_node(src, width=width)

            # HACK: Reference nodes cannot be attached to a section directly
            para = nodes.paragraph()

            src = get_source(dt_object, varname, zoom=2)
            para += get_link_node(src, "(zoom-level-2 [2.5km])")

            para += nodes.Text(" ", " ")

            src = get_source(dt_object, varname, zoom=3)
            para += get_link_node(src, "(zoom-level-3 [1.25km])")

            section_node += para
            node_list.append(section_node)

        return node_list


class VideoOverview(SphinxDirective):
    def run(self):
        src = pathlib.Path(self.env.srcdir)

        p = nodes.paragraph()
        p["classes"].append("multi-column")
        for doc in sorted((src / "lam").glob("*.md"), reverse=True):
            href = doc.relative_to(src, walk_up=True).with_suffix(".html").as_posix()
            datestr = datetime.fromisoformat(doc.stem).strftime("%Y-%m-%d")

            p += get_link_node(source_url=href, message=datestr)
            p += nodes.Text(" ", " ")

        return [p]


def setup(app):
    app.add_directive("lam-videos", LimitedAreaVideos)
    app.add_directive("list-videos", VideoOverview)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
