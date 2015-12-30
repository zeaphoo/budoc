
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

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def output(text):
    sys.stdout.write(text)
    sys.stdout.flush()

def budoc_all(bu_config, ident_name = None, **kwargs):
    for doc in bu_config.docs:
        module_name = doc['module']
        ident = doc.get('ident')
        dest = doc.get('dest')
        output('Generating %s%s api docs to %s\n'%(module_name, ':%s'%(ident) if ident else '', dest))
        try:
            md = budoc_one(module_name, ident_name=ident)
        except:
            output('    Error in generating.\n')
            continue
        output('    OK.\n')
        if dest and md:
            try:
                output('    Writing to %s.\n'%(dest))
                ensure_dir(dest)
                with open(dest, 'wb') as f:
                    f.write(md)
                output('    Done.\n')
            except:
                output('    Error in writing.\n')
                continue

def budoc_one(module_name, ident_name = None, **kwargs):
    stdout = kwargs.get('stdout', False)
    show_module = kwargs.get('show_module', False)
    docfilter = None
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

    module = pydoc.Module(module, docfilter=docfilter)
    doc = MarkdownGenerator(module).gen(module_doc=show_module)
    if stdout:
        sys.stdout.write(doc)
        sys.stdout.flush()
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


    def gen_variable(self, var, title_level=2):
        self.write('')
        self.write('%svar **%s**'%('#'*title_level, var.name))
        self.write('')
        self.write(var.docstring)

    def gen_function(self, func, title_level=2):
        write = self.write
        write('')
        write('%sdef **%s**(%s)'%('#'*title_level, func.name, func.spec()))
        write('')
        write(func.docstring)

    def gen_class(self, aclass, title_level=2):
        write = self.write
        init_method =  aclass.init_method() or NoneFunction()
        write('%sclass %s(%s)'%('#'*title_level, aclass.name, init_method.spec()))
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
                write('%svar **%s**'%('#'*(title_level+1), var.name))
                write('')
                write(var.docstring)

        if inst_vars:
            for var in inst_vars:
                write('')
                write('%svar **%s**'%('#'*(title_level+1), var.name))
                write('')
                write(var.docstring)

        if static_methods:
            for func in static_methods:
                write('')
                write('%sdef **%s**(%s)'%('#'*(title_level+1), func.name, func.spec()))
                write('')
                write(func.docstring)

        if methods:
            for func in methods:
                if func.name == '__init__':
                    continue
                write('')
                write('%sdef **%s**(%s)'%('#'*(title_level+1), func.name, func.spec()))
                write('')
                write(func.docstring)

    def gen(self, module_doc=True):
        module = self.module
        write = self.write
        if module_doc:
            write('#Module %s'%(module.name))
            if not module._filtering:
                write(module.docstring)

        title_level = 2 if module_doc else 1
        variables = module.variables()
        for var in variables:
            self.gen_variable(var, title_level=title_level)

        functions = module.functions()
        for func in functions:
            self.gen_function(func, title_level=title_level)

        classes = module.classes()
        for aclass in classes:
            self.gen_class(aclass, title_level=title_level)

        return '\n'.join(self.lines)
