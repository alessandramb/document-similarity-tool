import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

# Project information
project = 'Document Similarity Tool'
copyright = '2024, Alessandra Mastrobuono Battisti'
author = 'Your Name'
release = '1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML theme settings
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']

# Create the _static directory if it doesn't exist
if not os.path.exists('_static'):
    os.makedirs('_static')
