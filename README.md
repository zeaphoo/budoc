# budoc

Transfer python docstring to markdown.

Prominent features include:

* Support for documenting data representation by traversing the abstract syntax
  to find docstrings for module, class and instance variables.
* Usage is simple. Just write your documentation as Markdown. There are no
  added special syntax rules.
* Inheritance is used when possible to infer docstrings for class members.


`budoc` has been tested on Python 2.6, 2.7.


# Installation

`budoc` is [on PyPI](https://pypi.python.org/pypi/budoc) and is installable via
`pip`:

    pip install budoc



# Example usage

`budoc` will accept a Python module file, a yaml config file, package directory or an import path.
For example, to view the documentation for the `csv` module in the console:

    budoc csv

Or, you could view it by pointing at the file directly:

    budoc /usr/lib/python2.7/csv.py

Or, a document generating config file, in yaml format:

    budoc buconfig.yml

Submodules are fine too:

    budoc multiprocessing.pool

There are many other options to explore. You can see them all by running:

    budoc --help


# Example Config

```yaml
docs:
- module: budoc.pydoc
  ident: Module
  dest: docs/api_pydoc.md

- module: budoc.budoc
  dest: docs/api_budoc.md

```

# Docstring guideline

Docstring should be a simple Markdown format.

```python
# -*- coding: utf-8 -*-

example_variable = 12345
"""int: Module level variable documented inline.

The docstring may span multiple lines. The type may optionally be specified
on the first line, separated by a colon.
"""


def example_function(param1, param2=None, *args, **kwargs):
    """This is an example of a module level function.

    Function parameters should be documented in the `Args` section. The name
    of each parameter is required. The type and description of each parameter
    is optional, but should be included if not obvious.

    Parameter types -- if given -- should be specified according to
    `PEP 484`_, though `PEP 484`_ conformance isn't required or enforced.

    Args:

      * param1 (int): The first parameter.
      * param2 (Optional[str]): The second parameter. Defaults to None.
            Second line of description should be indented.
      * *args: Variable length argument list.
      * **kwargs: Arbitrary keyword arguments.

    Returns:

      * bool: True if successful, False otherwise.

    Raises:
      * AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
      * ValueError: If `param2` is equal to `param1`.


    .. _PEP 484:
       https://www.python.org/dev/peps/pep-0484/

    """
    if param1 == param2:
        raise ValueError('param1 may not be equal to param2')
    return True


def example_generator(n):
    """Generators have a ``Yields`` section instead of a ``Returns`` section.

    Args:

      * n (int): The upper limit of the range to generate, from 0 to `n` - 1.

    Yields:

      * int: The next number in the range of 0 to `n` - 1.

    Examples:
        >>> print([i for i in example_generator(4)])
        [0, 1, 2, 3]

    """
    for i in range(n):
        yield i


class ExampleError(Exception):
    """Exceptions are documented in the same way as classes.

    The __init__ method may be documented in either the class level
    docstring, or as a docstring on the __init__ method itself.

    Either form is acceptable, but the two should not be mixed. Choose one
    convention to document the __init__ method and be consistent with it.

    Note:

      Do not include the `self` parameter in the `Args` section.

    Args:

      * msg (str): Human readable string describing the exception.
      * code (Optional[int]): Error code.

    Attributes:

      * msg (str): Human readable string describing the exception.
      * code (int): Exception error code.

    """

    def __init__(self, msg, code):
        self.msg = msg
        self.code = code

```

# License

The MIT License (MIT).
