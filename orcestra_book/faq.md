# Technical FAQ

## How to create a local python environment?

The ORCESTRA book [repository](http://github.com/orcestra-campaign/book) comes
with an `environment.yml` that describes all Python packages that are needed to
build the website.  You can createa a Python environment with all dependencies by
using, e.g., `micromamba`:

```bash
micromamba env create -f environment.yml
```

## How to use the build environment in Jupyter lab?

If you are using Jupyter notebooks/lab to run Python code on your machine, you
can install the `orcestra_book` environment as an ipython kernel.

This way you can select `orcestra_book` as kernel to run your notebooks.

```bash
micromamba activate orcestra_book
ipython3 -m ipykernel install --user --name orcestra_book
```

## How to update the `orcestra_book` environment?

If you can't build your book, maybe some changes in the `environment.yml` were undertaken.
You can update the environment as following:

```bash
micromamba update env -f environment.yml
```

Please note, that sometimes a fresh install of the environment is a more robust approach.
Simply remove your existing environment by running:
```bash
micromamba env remove -n orcestra_book
```
and re-install it using the `environment.yaml`.
Your ipython kernels should still be able to find the "new" environment.

## Can I execute the notebooks interactively?

Yes, you can! The [MyST](https://mystmd.org) can be opened directly in
JupyterLab. Simply navigate to the location of the markdown file in the file
browser within JUpyterLab and right click `Open With > Notebook'. When you 
modify the notebook, the underlying markdown file is automatically synchronized.

_Note: This requires `jupterlab` and `jupytext` being installed, which if you 
are using an old environment might not be true._


## How to speedup execution of code cells

Some code cells (e.g. in flight planning) need to fetch data from external
servers. On slow Internet connections, this can increase the execution time of
your code cells.

You can speed this up by setting up a persistent local cache for `fsspec`. This
can be done by modifying (or creating) the `fsspec` configuration file
(`~/.config/fsspec/conf.json`):
```
{
  "simplecache": {
    "cache_storage": "/tmp/intake-cache"
  }
}
```
The above configuration enables a local cache in your `/tmp' directory. This
cache should be persistent across kernel reboots, but should still be flushed
by your operating system from time to time. You can use any other path if you
want a fully persistent cache.
