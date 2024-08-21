# Technical FAQ

## How to use the build environment in Jupyter lab?

If you are using Jupyter notebooks/lab to run Python code on your machine, you
can install the `orcestra_book` environment as an ipython kernel.

This way you can select `orcestra_book` as kernel to run your notebooks.

```bash
conda activate orcestra_book
ipython3 -m ipykernel install --user --name orcestra_book
```
