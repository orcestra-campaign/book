# The ORCESTRA book

This repo collects all information to the ORCESTRA campaign in the form of a book. For now, the rendered book (website) is deployed to **https://orcestra-campaign.org/**

The book is thought to grow and include information on
* the **science**
* the measurement **strategy**
* **data**, including a data concept, data policy, data access and description
* the **flight planning** and **reports**
* and much more...

## Building the book

You can build the book from within the repo's root folder by running:

```sh
jupyter-book build orcestra_book/
```

A fully-rendered HTML version of the book will be built in `orcestra-book/_build/html/`.
You can have a look at it by opening the `_build/html/index.html` file in your browser.

In case the book builds without errors, but your changes don't seem to get rendered it might be due to the cache.
You can force the book to be built from scratch by removing the existing `orcestra-book/_build/` directory before building the book.

## Contributing

This is a project from the community for you and for the community and it is under constant improvement. Everyone is welcome to contribute with scripts, ideas, suggestions, by opening issues and making pull requests. More details can be found [here](CONTRIBUTING.md).

## Credits

This project is created using the excellent open source [Jupyter Book project](https://jupyterbook.org/) and the [executablebooks/cookiecutter-jupyter-book template](https://github.com/executablebooks/cookiecutter-jupyter-book).
