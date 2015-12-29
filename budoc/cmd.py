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

from . import budoc
from .config import load_config

# `xrange` is `range` with Python3.
try:
    xrange = xrange
except NameError:
    xrange = range

parser = argparse.ArgumentParser(
    description='Automatically generate API docs for Python modules.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
aa = parser.add_argument
aa('module_or_config', type=str, nargs='?',
   help='The Python module name Or Config file. '
        'May be an import path resolvable in the current environment, '
        'OR a file path to a Python module or package, '
        'OR path of config file.', default='budoc.yml')

aa('ident_name', type=str, nargs='?',
   help='When specified, only identifiers containing the name given '
        'will be shown in the output. Search is case sensitive. ')

aa('--version', action='store_true',
   help='Print the version of budoc and exit.')

args = parser.parse_args()

def run():
    if args.version:
        print('budoc %s'%(budoc.__version__))
        sys.exit(0)

    # We close stdin because some modules, upon import, are not very polite
    # and block on stdin.
    try:
        sys.stdin.close()
    except:
        pass

    module_or_config = args.module_or_config
    name, ext = os.path.splitext(module_or_config)
    if ext == '' or ext.lower() == '.py':
        budoc.budoc_one(args.module_or_config, args.ident_name, stdout=True)
    else:
        try:
            bu_config = load_config(module_or_config)
        except:
            print('Config file %s not exits or not valid yaml format.'%(module_or_config))
            sys.exit(-1)
        budoc.budoc_all(bu_config, args.ident_name)


if __name__ == '__main__':
    run()
