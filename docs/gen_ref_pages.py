"""
Generate the code reference pages and navigation.

Based on https://mkdocstrings.github.io/recipes/#automatic-code-reference-pages
"""

import logging
import os
from pathlib import Path

import mkdocs_gen_files


IGNORED_DIRECTORIES = {"migrations", "test"}
"""
Directories that will not be added to the documentation.
"""

TRUE_CHOICES = "true,1,t,y,yes,yeah,yup,certainly,uh-huh".split(",")
"""
Values corresponding to true.
"""


logger = logging.getLogger("meringue")


def sort_key(item: Path):
    """
    Mthod to sort directories and filter ignored
    """
    return item.is_dir() and not (set(item.parts) & IGNORED_DIRECTORIES)


def directory_processing(path: Path, doc_section: str, nav: mkdocs_gen_files.Nav):
    """
    Function looks for files in the specified directory and registers them in the documentation.

    Args:
        path: Source directory.
        doc_section: Section in documentation for registering new sections.
        nav: Nav object where the files will be registered.
    """

    # processing subdirectories
    directories = list(filter(sort_key, path.glob("*")))
    for directory in directories:
        directory_processing(directory, doc_section, nav)

    # files processing
    files = sorted(filter(lambda i: i.is_file(), path.glob("*.py")))
    for file in files:
        parts = tuple(file.parts)

        if parts[-1] == "__main__.py":
            continue

        if not parts[-1].endswith(".py"):
            continue

        doc_file = file.with_suffix(".md")
        doc_path = doc_section / doc_file

        # add file to navigation
        nav[parts[1:]] = doc_file.as_posix()

        # write markdown file
        module_to_parse = parts[:-1]
        if parts[-1] != "__init__.py":
            module_to_parse += (doc_file.stem,)

        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"::: {'.'.join(module_to_parse)}\n")
            fd.write("\toptions:\n")
            # fd.write("\t\tshow_if_no_docstring: true\n")
            fd.write("\t\theading_level: 1\n")
            fd.write("\t\tshow_root_heading: true\n")
            fd.write("\t\tmembers_order: source\n")

        mkdocs_gen_files.set_edit_path(doc_path, Path("../") / path)


def generate_code_section():
    """
    Function for parsing the source folder and registering files in the documentation
    """
    if os.environ.get("MERINGUE_MKDOCS_CODE_PARCE_ENABLED", "t").lower() not in TRUE_CHOICES:
        return

    # parse and register
    source_path = Path(os.environ.get("MERINGUE_MKDOCS_CODE_PARCE_SOURCE_PATH", "meringue"))
    doc_path = Path(os.environ.get("MERINGUE_MKDOCS_CODE_PARCE_DOCS_PATH", "reference"))
    nav = mkdocs_gen_files.Nav()
    directory_processing(source_path, doc_path, nav)

    # make navigration
    with mkdocs_gen_files.open(doc_path / "SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())

    # show navigation for debug
    if os.environ.get("MERINGUE_MKDOCS_CODE_PARCE_SHOW_NAV", "f").lower() in TRUE_CHOICES:
        with mkdocs_gen_files.open(doc_path / "SUMMARY.md", "r") as nav_file:
            logger.info(nav_file.read())


# start generation of docs from code
generate_code_section()
