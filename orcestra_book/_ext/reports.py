import pathlib
import re
from collections import defaultdict
from functools import lru_cache

import yaml
from jinja2 import Template


@lru_cache
def load_frontmatter(path):
    """Load and return the front matter section of a YAML file."""
    print(path)
    with open(path, "r") as fp:
        frontmatter = next(yaml.safe_load_all(fp))

    frontmatter["filepath"] = path.as_posix()

    return frontmatter


def fpath2id(fpath):
    """Extract the ID (e.g. HALO-20240801a) from a given file path."""
    return pathlib.Path(fpath).stem


def collect_all_metadata(src, subdirs=("plans", "reports"), pattern="*.md"):
    """Collect front matter from Markdown files in various given locations."""
    metadata = defaultdict(dict)
    for subdir in subdirs:
        for src_file in (src / subdir).glob(pattern):
            subdir = (
                subdir[:-1] if subdir.endswith("s") else subdir
            )  # e.g. plans -> plan
            metadata[fpath2id(src_file)][subdir] = load_frontmatter(src_file)

    return metadata


def consolidate_metadata(src, metadata):
    """Merge duplicated data from flight plans and reports."""
    latest_source = "report" if "report" in metadata else "plan"

    for key in ("takeoff", "landing", "crew", "nickname"):
        metadata[key] = metadata[latest_source].get(key, None)
    for key in ("categories",):
        metadata[key] = metadata[latest_source].get(key, [])

    metadata["pi"] = [
        member["name"] for member in metadata["crew"] if member["job"].lower() == "pi"
    ][0]

    # Collect relative Sphinx links to flight plans and reports
    refs = []
    for k, v in metadata.items():
        if isinstance(v, dict) and "filepath" in v:
            relpath = pathlib.Path(v["filepath"]).relative_to(
                src / "operation", walk_up=True
            )
            refs.append(f"[{k}]({relpath})")

    metadata["refs"] = refs

    return metadata


def write_ship_table(app):
    """Collect all reports from RV METEOR and create an overview table."""
    src = pathlib.Path(app.srcdir)
    metadata = collect_all_metadata(src)

    regex = re.compile("METEOR-[0-9]*")
    # For now, only shipd **reports** are expected. May need to be adapted in future.
    frontmatters = {k: v["report"] for k, v in metadata.items() if regex.match(k)}

    with open(src / "_templates" / "operation_rvmeteor.md", "r") as fp:
        templ = fp.read()

    with open(src / "operation" / "rvmeteor.md", "w") as fp:
        t = Template(templ)
        fp.write(t.render(reports=frontmatters))


def write_flight_table(app=None):
    """Collect all reports from HALO and create an overview table."""
    # src = pathlib.Path(app.srcdir)
    src = pathlib.Path("orcestra_book/")
    metadata = collect_all_metadata(src)

    regex = re.compile("HALO-[0-9]*[a-z]")
    frontmatters = {
        k: consolidate_metadata(src, v) for k, v in metadata.items() if regex.match(k)
    }
    print(frontmatters["HALO-20240810a"]["refs"])

    with open(src / "_templates" / "operation_halo.md", "r") as fp:
        templ = fp.read()

    with open(src / "operation" / "halo.md", "w") as fp:
        t = Template(templ)
        fp.write(t.render(flights=frontmatters))


def setup(app):
    app.connect("builder-inited", write_flight_table)
    app.connect("builder-inited", write_ship_table)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
