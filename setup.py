#!/usr/bin/env python
"""
Distutils based setup script for geometric-integration

This uses Distutils (http://python.org/sigs/distutils-sig/) the standard
python mechanism for installing packages. For the easiest installation
just type the command (you'll probably need root privileges for that):

    python setup.py install

This will install the library in the default location. To install in a
custom directory <dir>, use

    python setup.py --prefix=<dir>
"""

__version__ = '0.1'

from distutils.core import setup, Command
from distutils.extension import Extension
from Cython.Distutils import build_ext
import unittest
import os
import os.path
import numpy


class clean(Command):
    """
    Cleans *.pyc and other trash files producing the same copy of the code
    as in the git repository.
    """
    description = "remove all build and trash files"
    user_options = []
    cleaned_file_extensions = ['.pyc', '~', '.so', '.c', '.html']
    ignored_files = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # helper function for deleting directory and contents
        def delete_dir(dir):
            # don't do anything if directory already doesn't exist
            if not os.path.isdir(dir):
                return

            # dive into directory contents. if file, delete.
            # if directory, run delete_dir.
            for f in os.listdir(dir):
                path = os.path.join(dir,f)
                try:
                    if os.path.isfile(path):
                        os.remove(path)
                    elif os.path.isdir(path):
                        delete_dir(path)
                        os.removedirs(path)
                except Exception, e:
                    print e

        # deletes .pyc files that don't have corresponding .py files
        to_remove = []
        for root, dirs, files in os.walk('.'):
            # get absolute path to each file
            files = map(lambda f: os.path.join(root,f), files)

            # filter out various file types
            for ext in self.cleaned_file_extensions:
                to_remove.extend(filter(lambda f: f.endswith(ext), files))

        # make sure ignored files are removed from the 'to remove' list
        for f in self.ignored_files:
            to_remove.remove(f)

        # delete the files slated for removal
        for f in to_remove:
            os.unlink(f)

        # delete build directories
        dirs = ['./build', './doc/build']
        for d in dirs:
            delete_dir(d)


class test_geomint(Command):
    """
    Runs all tests under every geomint/ directory.
    """
    description = "run all tests and doctests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        loader = unittest.TestLoader()
        suite = loader.discover('geomint')
        unittest.TextTestRunner(verbosity=2).run(suite)

packages = []
ext_modules = []

tests = [
    'geometric_integration.tests',
    ]

classifiers = [
    'Programming Language :: Python',
    'Programming Language :: Cython',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Scientific/Engineering :: Physics',
    'Intended Audience :: Science/Research',
    'Operating System :: Unix',
    'Operating System :: MaxOS'
    ]

long_description = '''Implementations of ODE Solvers from Geometric Numerical
Integration by Harier, et. al.'''

setup(
    name = 'geomint',
    version = __version__,
    description = 'Implementations of ODE Solvers from Geometric Numerical '
                   'Integration by Harier, et. al.',
    long_description = long_description,
    author = 'Chris Swierczewski',
    author_email = 'cswiercz@gmail.com',
    url = 'https://github.com/nonlinear-waves-seattle/geometric-integration',
    license = 'GPL v2+',
    packages = ['geomint'] + packages + tests,
    ext_modules = ext_modules,
    cmdclass = {'test': test_geomint,
                'clean': clean,
                'build_ext': build_ext
                },
    platforms = ['Linux', 'Unix', 'Mac OS-X'],
    classifiers = classifiers,
    )
