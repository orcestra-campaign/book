# Technical FAQ

## How to use the build environment in Jupyter lab?

If you are using Jupyter notebooks/lab to run Python code on your machine, you
can install the `orcestra_book` environment as an ipython kernel.

This way you can select `orcestra_book` as kernel to run your notebooks.

```bash
conda activate orcestra_book
ipython3 -m ipykernel install --user --name orcestra_book
```

## How to update the orcestra_book environmeny?

If you can't build your book, maybe some changes in the `environment.yml` were undertaken.
You can update the environment as following:

```bash
conda update env -f environment.yml
```

## Can I execute the notebooks interactively?

Yes, you can! The [MyST](https://mystmd.org) can be opened directly in
JupyterLab. Simply navigate to the location of the markdown file in the file
browser within JUpyterLab and right click `Open With > Notebook'. When you 
modify the notebook, the underlying markdown file is automatically synchronized.

_Note: This requires `jupterlab` and `jupytext` being installed, which if you 
are using an old environment might not be true._
