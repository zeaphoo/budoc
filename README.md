# budoc

Transfer python docstring to markdown.

Prominent features include:

* Support for documenting data representation by traversing the abstract syntax
  to find docstrings for module, class and instance variables.
* Usage is simple. Just write your documentation as Markdown. There are no
  added special syntax rules.
* `budoc` respects your `__all__` variable when present.
* Inheritance is used when possible to infer docstrings for class members.

The above features are explained in more detail in budoc's documentation.

`budoc` has been tested on Python 2.6, 2.7.


# Installation

`budoc` is [on PyPI](https://pypi.python.org/pypi/budoc) and is installable via
`pip`:

    pip install budoc

# Example Config

```
docs:
- module: budoc.pydoc
  ident: Module
  dest: docs/api_pydoc.md

- module: budoc.budoc
  dest: docs/api_budoc.md


```

# Example usage

`budoc` will accept a Python module file, package directory or an import path.
For example, to view the documentation for the `csv` module in the console:

    budoc csv

Or, you could view it by pointing at the file directly:

    budoc /usr/lib/python2.7/csv.py

Submodules are fine too:

    budoc multiprocessing.pool

There are many other options to explore. You can see them all by running:

    budoc --help


# License

The MIT License (MIT).
