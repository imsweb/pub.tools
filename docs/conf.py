from importlib.metadata import version as meta_version

project = 'pub.tools'
copyright = '2024, Eric Wohnlich'
author = 'Eric Wohnlich'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_tabs.tabs',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.md': 'markdown',
}

version = meta_version('pub.tools')

html_theme = 'sphinx_rtd_theme'
