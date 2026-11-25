# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'NXOpenKit'
copyright = '2026, Shashi Kant'
author = 'Shashi Kant'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys
import shutil
import subprocess
from pathlib import Path

#sys.path.insert(0, os.path.abspath('../src'))

extensions = [
    "myst_parser",
    "sphinxcontrib.mermaid",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.graphviz",
    "sphinx_copybutton",
]

source_suffix = {
    ".md": "markdown",
}


templates_path = ['_templates']
exclude_patterns = []

# graphviz_dot = r"C:\Program Files\Graphviz\bin\dot.exe"
# graphviz_output_format = "svg"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_css_files = ['custom.css']
html_theme_options = {
    "navigation_with_keys": True,
    "top_of_page_button": "edit",
    "light_css_variables": {
        "color-brand-primary": "#2563eb",
        "color-brand-content": "#2563eb",
    },
}

add_module_names = False
autodoc_class_signature = "separated"
autodoc_typehints = "signature"
autodoc_typehints_format = "short"
python_use_unqualified_type_names = True
toc_object_entries = True
toc_object_entries_show_parents = "hide"

DOCS_DIR = Path(__file__).resolve().parent
DOXYGEN_DIR = DOCS_DIR / "doxygen"
DOXYGEN_HTML = DOCS_DIR / "_build" / "api" / "html"


def build_doxygen(app):
    """Generate the Doxygen API documentation before the Sphinx HTML build."""
    if app.builder.name != "html":
        return
    subprocess.run(["doxygen", "Doxyfile"], cwd=DOXYGEN_DIR, check=True)


def copy_doxygen_to_sphinx(app, exception):
    """Copy generated Doxygen HTML into the completed Sphinx output directory."""
    if app.builder.name != "html" or exception or not DOXYGEN_HTML.is_dir():
        return

    destination = Path(app.outdir) / "doxygen"
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(DOXYGEN_HTML, destination)


def setup(app):
    app.connect("builder-inited", build_doxygen)
    app.connect("build-finished", copy_doxygen_to_sphinx)

copybutton_prompt_text = r">>> |\\$ "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = False
