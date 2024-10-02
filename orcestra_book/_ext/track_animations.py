from docutils import nodes
from sphinx.util.docutils import SphinxDirective


SWIFT_CONTAINER = "https://swift.dkrz.de/v1/dkrz_948e7d4bbfbb445fbff5315fc433e36a/ORCESTRA/static/flight_animations"


class TrackAnimation(SphinxDirective):
    option_spec = {
        "flight_id": str,
        "width": int,
        "justify": str,
    }

    def run(self):
        flight_id = self.options["flight_id"]
        width = self.options.get("width", 576)
        justify = self.options.get("justify", "center")

        source = f"<source src={SWIFT_CONTAINER}/{flight_id}.mp4>"
        err = "Your browser does not support the video tag."
        video = f"<video width='{width}' controls>{source} type='mp4'/>{err}</video>"
        centered_video = (
            f"<div style='display: flex; justify-content: {justify};'>{video}</div>"
        )

        raw_node = nodes.raw(
            rawsource="",
            text=centered_video,
            format="html",
        )

        return [raw_node]


def setup(app):
    app.add_directive("track-animation", TrackAnimation)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
