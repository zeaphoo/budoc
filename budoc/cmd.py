#!/usr/bin/env python2

from __future__ import absolute_import, division, print_function
import argparse
import codecs
import datetime
import imp
import os
import os.path as path
import pkgutil
import re
import subprocess
import sys
import tempfile

import pdoc

# `xrange` is `range` with Python3.
try:
    xrange = xrange
except NameError:
    xrange = range

version_suffix = '%d.%d' % (sys.version_info[0], sys.version_info[1])
default_http_dir = path.join(tempfile.gettempdir(), 'pdoc-%s' % version_suffix)

parser = argparse.ArgumentParser(
    description='Automatically generate API docs for Python modules.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
aa = parser.add_argument
aa('module_name', type=str, nargs='?',
   help='The Python module name. This may be an import path resolvable in '
        'the current environment, or a file path to a Python module or '
        'package.')
aa('ident_name', type=str, nargs='?',
   help='When specified, only identifiers containing the name given '
        'will be shown in the output. Search is case sensitive. '
        'Has no effect when --http is set.')
aa('--version', action='store_true',
   help='Print the version of pdoc and exit.')
aa('--all-submodules', action='store_true',
   help='When set, every submodule will be included, regardless of whether '
        '__all__ is set and contains the submodule.')
aa('--only-pypath', action='store_true',
   help='When set, only modules in your PYTHONPATH will be documented.')
args = parser.parse_args()


def quick_desc(imp, name, ispkg):
    if not hasattr(imp, 'path'):
        # See issue #7.
        return ''

    if ispkg:
        fp = path.join(imp.path, name, '__init__.py')
    else:
        fp = path.join(imp.path, '%s.py' % name)
    if os.path.isfile(fp):
        with codecs.open(fp, 'r', 'utf-8') as f:
            quotes = None
            doco = []
            for i, line in enumerate(f):
                if i == 0:
                    if len(line) >= 3 and line[0:3] in ("'''", '"""'):
                        quotes = line[0:3]
                        line = line[3:]
                    else:
                        break
                line = line.rstrip()
                if line.endswith(quotes):
                    doco.append(line[0:-3])
                    break
                else:
                    doco.append(line)
            desc = '\n'.join(doco)
            if len(desc) > 200:
                desc = desc[0:200] + '...'
            return desc
    return ''


def _eprint(*args, **kwargs):
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)


def last_modified(fp):
    try:
        return datetime.datetime.fromtimestamp(os.stat(fp).st_mtime)
    except:
        return datetime.datetime.min


def module_file(m):
    mbase = path.join(args.html_dir, *m.name.split('.'))
    if m.is_package():
        return path.join(mbase, pdoc.html_package_name)
    else:
        return '%s%s' % (mbase, pdoc.html_module_suffix)



def run():
    if args.version:
        print(pdoc.__version__)
        sys.exit(0)

    # We close stdin because some modules, upon import, are not very polite
    # and block on stdin.
    try:
        sys.stdin.close()
    except:
        pass

    if not args.http and args.module_name is None:
        _eprint('No module name specified.')
        sys.exit(1)
    if args.template_dir is not None:
        pdoc.tpl_lookup.directories.insert(0, args.template_dir)
    if args.http:
        args.html = True
        args.external_links = True
        args.html_dir = args.http_dir
        args.overwrite = True
        args.link_prefix = '/'

    # If PYTHONPATH is set, let it override everything if we want it to.
    pypath = os.getenv('PYTHONPATH')
    if args.only_pypath and pypath is not None and len(pypath) > 0:
        pdoc.import_path = pypath.split(path.pathsep)

    docfilter = None
    if args.ident_name and len(args.ident_name.strip()) > 0:
        search = args.ident_name.strip()

        def docfilter(o):
            rname = o.refname
            if rname.find(search) > -1 or search.find(o.name) > -1:
                return True
            if isinstance(o, pdoc.Class):
                return search in o.doc or search in o.doc_init
            return False

    # Try to do a real import first. I think it's better to prefer
    # import paths over files. If a file is really necessary, then
    # specify the absolute path, which is guaranteed not to be a
    # Python import path.
    try:
        module = pdoc.import_module(args.module_name)
    except Exception as e:
        module = None

    # Get the module that we're documenting. Accommodate for import paths,
    # files and directories.
    if module is None:
        isdir = path.isdir(args.module_name)
        isfile = path.isfile(args.module_name)
        if isdir or isfile:
            fp = path.realpath(args.module_name)
            module_name = path.basename(fp)
            if isdir:
                fp = path.join(fp, '__init__.py')
            else:
                module_name, _ = path.splitext(module_name)

            # Use a special module name to avoid import conflicts.
            # It is hidden from view via the `Module` class.
            with open(fp) as f:
                module = imp.load_source('__pdoc_file_module__', fp, f)
                if isdir:
                    module.__path__ = [path.realpath(args.module_name)]
                module.__pdoc_module_name = module_name
        else:
            module = pdoc.import_module(args.module_name)
    module = pdoc.Module(module, docfilter=docfilter,
                         allsubmodules=args.all_submodules)

    # Plain text?
    if not args.html:
        output = module.text()
        try:
            print(output)
        except IOError as e:
            # This seems to happen for long documentation.
            # This is obviously a hack. What's the real cause? Dunno.
            if e.errno == 32:
                pass
            else:
                raise e
        sys.exit(0)

if __name__ == '__main__':
    run()
