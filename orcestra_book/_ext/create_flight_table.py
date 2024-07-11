#!/usr/bin/env python3
import os
import pathlib
import subprocess
from datetime import datetime

from frontmatter import Frontmatter
from jinja2 import Template


templ = """<!-- This file was created automatically -->
# Operation

Flight-ID | Date | Takeoff | Landing | PI | Nickname | Objectives
--- | --- | --- | --- | --- | --- | ---
{% for k, v in flights.items() -%}
[](flight_reports/{{ k }}) | {{ v["expr_date"] }} | {{ v["expr_takeoff"] }} | {{ v["expr_landing"] }} | {{ v["pi"] }} | {{ v["nickname"] }} | {{ v["objectives"]|join(', ') }}
{% endfor -%}
"""


def read_frontmatter(path):
    attrs = Frontmatter.read_file(path)["attributes"]

    takeoff = datetime.fromisoformat(attrs["takeoff"])
    landing = datetime.fromisoformat(attrs["landing"])

    attrs["expr_date"] = takeoff.strftime("%d %B %Y")
    attrs["expr_takeoff"] = takeoff.strftime("%X")
    attrs["expr_landing"] = landing.strftime("%X")

    return attrs


def collect_fronmatter():
    flights = pathlib.Path("orcestra_book/flight_reports/").glob("*[0-9]*[a-z].md")
    return {fm["flight_id"]: fm for fm in map(read_frontmatter, sorted(flights))}


def write_flight_table(app, path="orcestra_book/operation.md"):
    frontmatters = collect_fronmatter()

    with open(path, "w") as fp:
        t = Template(templ)
        fp.write(t.render(flights=frontmatters))


def setup(app):
    app.connect('builder-inited', write_flight_table)
