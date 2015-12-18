
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

import re

def indent(s, spaces=4):
    """
    Inserts `spaces` after each string of new lines in `s`
    and before the start of the string.
    """
    new = re.sub('(\n+)', '\\1%s' % (' ' * spaces), s)
    return (' ' * spaces) + new.strip()

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
    doc = MarkdownGenerator(module).gen()
    print(doc)
    return doc

class NoneFunction(object):
    def __init__(self):
        self.docstring = ''
        
    def spec(self):
        return ''

class MarkdownGenerator(object):
    def __init__(self, module):
        self.lines = []
        self.write = self.lines.append
        self.module = module


    def gen_variable(self, var):
        self.write('')
        self.write('##var **%s**'%(var.name))
        self.write('')
        self.write(var.docstring)

    def gen_function(self, func):
        write = self.write
        write('')
        write('##def **%s**(%s)'%(func.name, func.spec()))
        write('')
        write(func.docstring)

    def gen_class(self, aclass):
        write = self.write
        init_method =  aclass.init_method() or NoneFunction()
        write('##class %s(%s)'%(aclass.name, init_method.spec()))
        write('')
        write(aclass.docstring)
        write(init_method.docstring)
        class_vars = aclass.class_variables()
        static_methods = aclass.functions()
        methods = aclass.methods()
        inst_vars = aclass.instance_variables()

        if class_vars:
            for var in class_vars:
                write('')
                write('###var **%s**'%(var.name))
                write('')
                write(var.docstring)

        if inst_vars:
            for var in inst_vars:
                write('')
                write('###var **%s**'%(var.name))
                write('')
                write(var.docstring)

        if static_methods:
            for func in static_methods:
                write('')
                write('###def **%s**(%s)'%(func.name, func.spec()))
                write('')
                write(func.docstring)

        if methods:
            for func in methods:
                if func.name == '__init__':
                    continue
                write('')
                write('###def **%s**(%s)'%(func.name, func.spec()))
                write('')
                write(func.docstring)

    def gen(self):
        module = self.module
        write = self.write
        write('#Module %s'%(module.name))
        if not module._filtering:
            write(module.docstring)

        variables = module.variables()
        for var in variables:
            self.gen_variable(var)

        functions = module.functions()
        for func in functions:
            self.gen_function(func)

        classes = module.classes()
        for aclass in classes:
            self.gen_class(aclass)

        return '\n'.join(self.lines)
