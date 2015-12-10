"""
A command line tool and library to auto generate API documentation to Markdown file for Python libraries.
"""

from __future__ import print_function
import sys
from setuptools import setup

setup(
    name='budoc',
    version='0.1',
    url='http://github.com/zeaphoo/budoc/',
    download_url='http://github.com/zeaphoo/cocopot/budoc/0.1',
    license='BSD',
    author='zeaphoo',
    author_email='zeaphoo@gmail.com',
    description='A command line tool and library to auto generate API documentation to Markdown file for Python libraries.',
    long_description=__doc__,
    packages=['budoc'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'budoc = budoc.cmd:run']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
