import os
import sys

project = 'pub.tools'
copyright = '2022, Eric Wohnlich'
author = 'Eric Wohnlich'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_tabs.tabs',
    'sphinxarg.ext'
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.md': 'markdown',
}

eggs = os.environ.get('BUILDOUT_EGGS', None)
if eggs:
    src_eggs = os.listdir(os.path.join(eggs, '..', 'src'))
    for egg in os.listdir(eggs):
        sys.path.insert(0, os.path.join(eggs, egg))
    for egg in src_eggs:
        sys.path.insert(0, os.path.join(eggs, '..', 'src', egg))

imsplone_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, imsplone_root)

venv = os.environ.get('VIRTUAL_ENV', None)
if venv:
    sys.path.insert(0, os.path.join(venv, 'Lib', 'site-packages'))

# html_logo = 'images/plone.png'
# html_favicon = 'images/favicon.ico'

with open(os.path.join('..', 'VERSION.txt')) as fopen:
    version = fopen.read().strip()

html_theme ='sphinx_rtd_theme'
html_domain_indices = True