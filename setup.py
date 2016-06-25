"""A setuptools based setup module for SnakeTeX"""

from setuptools import setup, find_packages
from codecs import open
from os import path, remove, system
from shutil import copyfile

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SnakeTeX',
    version='0.1.2',
    description='A LaTeX template system for large and multi-user projects.',
    install_requires=['Click', 'jinja2', 'PyYAML'],
    entry_points={'console_scripts': ['stex=snaketex.stex:main']},
    packages=find_packages(exclude=['example', 'docs', 'tests*']),
    license='GPLv3',
    author='Olivier Pieters',
    author_email='me@olivierpieters.be',
    url='https://github.com/opieters/SnakeTeX',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Text Processing :: Markup :: LaTeX',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=['LaTeX TeX XeTeX documents template system'],
    package_data={'snaketex': ['*.stex']}
)
