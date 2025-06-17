
import os
import sys

sys.path.insert(0, os.path.abspath('../../src/'))

project = 'Y360 Library'
copyright = '2025, Anton Bugrin'
author = 'Anton Bugrin'
release = '0.0.8'


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



html_theme = 'sphinx_rtd_theme'
#html_static_path = ['_static']

autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
