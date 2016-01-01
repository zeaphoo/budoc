"""
A command line tool and library to auto generate API documentation to Markdown file for Python libraries.
"""

from __future__ import print_function
import sys
from setuptools import setup

setup(
    name='budoc',
    version='0.2',
    url='http://github.com/zeaphoo/budoc/',
    download_url='http://github.com/zeaphoo/budoc/tarball/0.1',
    license='BSD',
    author='zeaphoo',
    author_email='zeaphoo@gmail.com',
    description='A command line tool and library to auto generate API documentation to Markdown file for Python libraries.',
    long_description=__doc__,
    packages=['budoc'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['PyYAML'],
    entry_points={
        'console_scripts': [
            'budoc = budoc.cmd:run']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
