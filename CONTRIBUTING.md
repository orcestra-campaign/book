# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given. You can contribute in the ways listed below.

## Report Bugs

Report bugs using GitHub issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

## Fix Bugs and Implement Features

Look through the GitHub issues for bugs and features. Anything tagged with "bug", "help
wanted" or "enhancement" is open to whoever wants to implement it.

## Write Documentation

The ORCESTRA book could always use more documentation, whether through describing a
a sub-campaign or an instrument measurement or by adding a data processing example.
Please feel free to add information yourself or open an issue if you lack the time 
or knowledge to add it right away.


## Get Started

Ready to contribute? Here's how to set up the `ORCESTRA book` for local development.

1. Fork the repo on GitHub.
2. Clone your fork locally.
3. Install your local copy into a virtualenv, e.g., using `conda`: `conda env create -f environment.yml`.
4. Create a branch for local development and make changes locally.
5. Build the book locally to see if the fully-rendered HTML version looks as intended (see below how to).
6. Commit your changes and push your branch to GitHub.
7. Submit a pull request through the GitHub website.

## Building the book

To check your changes locally you can build the book from within the repo's root folder:

```
jupyter-book build orcestra-book/
```

A fully-rendered HTML version of the book will be built in `orcestra-book/_build/html/`.
You can have a look at it by opening the `_build/html/index.html` file in your browser.
In case the book builds without errors, but your changes don't seem to get rendered it might be due to the cache.
You can force the book to be built from scratch by removing the existing `orcestra-book/_build/` directory before building the book.

## Code of Conduct

Please note that the ORCESTRA book project is released with a [Contributor Code of Conduct](CONDUCT.md). By contributing to this project you agree to abide by its terms.
