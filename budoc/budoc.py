
from __future__ import absolute_import, division, print_function
import ast
import imp
import inspect
import os
import os.path as path
import pkgutil
import re
import sys
from . import pydoc


def budoc_one(module_name, ident_name = None, **kwargs):
    docfilter = None
    all_submodules = kwargs.get('all_submodules')
    if ident_name and len(ident_name.strip()) > 0:
        search = ident_name.strip()

        def docfilter(o):
            rname = o.refname
            if rname.find(search) > -1 or search.find(o.name) > -1:
                return True
            if isinstance(o, pydoc.Class):
                return search in o.doc or search in o.doc_init
            return False
    # Try to do a real import first. I think it's better to prefer
    # import paths over files. If a file is really necessary, then
    # specify the absolute path, which is guaranteed not to be a
    # Python import path.
    try:
        module = pydoc.import_module(module_name)
    except Exception as e:
        module = None

    # Get the module that we're documenting. Accommodate for import paths,
    # files and directories.
    if module is None:
        isdir = path.isdir(module_name)
        isfile = path.isfile(module_name)
        if isdir or isfile:
            fp = path.realpath(module_name)
            module_name = path.basename(fp)
            if isdir:
                fp = path.join(fp, '__init__.py')
            else:
                module_name, _ = path.splitext(module_name)

            # Use a special module name to avoid import conflicts.
            # It is hidden from view via the `Module` class.
            with open(fp) as f:
                module = imp.load_source('__budoc_file_module__', fp, f)
                if isdir:
                    module.__path__ = [path.realpath(module_name)]
                module.__pydoc_module_name = module_name
        else:
            module = pydoc.import_module(module_name)
        module = pydoc.Module(module, docfilter=docfilter,
                         allsubmodules=all_submodules)
        return gen_markdown(module)


def gen_markdown_variable(variable):
    pass

def gen_markdown_function(function):
    pass

def gen_markdown_class(cls):
    pass

def gen_markdown_module(module):
    lines = []
    write = lines.append
    write('# Module %s'%(module.name))
    if not module._filtering:
        write(module.docstring)

    variables = module.variables()
    write('## Variables')
    for var in variables:
        write()

    return '\n'.join(lines)
