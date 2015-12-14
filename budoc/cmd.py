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

import budoc

# `xrange` is `range` with Python3.
try:
    xrange = xrange
except NameError:
    xrange = range

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
   help='Print the version of budoc and exit.')
aa('--all-submodules', action='store_true',
   help='When set, every submodule will be included, regardless of whether '
        '__all__ is set and contains the submodule.')

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

    if not args.module_name:
        parser.print_help()
        sys.exit(0)
    budoc.budoc_one(args.module_name, args.ident_name, allsubmodules=args.all_submodules)


if __name__ == '__main__':
    run()
