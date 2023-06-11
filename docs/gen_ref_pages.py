"""
Generate the code reference pages and navigation.

Based on https://github.com/mkdocstrings/mkdocstrings/blob/cd9e62062766ddb14ab16b6d6eaeb3d751dbe417/docs/gen_ref_nav.py
"""

from pathlib import Path
import os

import mkdocs_gen_files


IGNORED_DIRECTORIES = {'migrations', 'test'}

TRUE_CHOICES = "true,1,t,y,yes,yeah,yup,certainly,uh-huh".split(',')


def sort_key(item):
    return os.path.isdir(item) and not (set(item.parts) & IGNORED_DIRECTORIES)


def directory_processing(path: Path, doc_section: str, nav: 'Nav'):
    """
    Function looks for files in the specified directory and registers them in the documentation

    Args:
        path: Source directory
        doc_section: Section in documentation for registering new sections
        nav: Nav object where the files will be registered
    """
    # doc_path_bits = tuple(doc_section.parts)
    # print(Path(doc_section, 'catalogue/test.md'))
    # print(doc_section, / 'catalogue/test.md')

    directories = list(filter(sort_key, path.glob('*')))
    files = list(sorted(filter(os.path.isfile, path.glob('*.py'))))

    for directory in directories:
        directory_processing(directory, doc_section, nav)

    for file in files:
        parts = tuple(file.parts)

        if parts[-1] == "__main__.py":
            # ignore __main__ file
            continue

        doc_relative_path = file.with_suffix(".md")  # ???
        full_doc_path = doc_section / doc_relative_path

        # fill nav
        nav[parts[1:]] = doc_relative_path.as_posix()

        # write markdown file
        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            if parts[-1] == '__init__.py':
                parts = parts[:-1]

            elif parts[-1].endswith('.py'):
                parts = parts[:-1] + (parts[-1][:-3], )

            ident = ".".join(parts)
            fd.write(f"::: {ident}\n")
            fd.write("\toptions:\n")
            # fd.write("\t\tshow_if_no_docstring: true\n")
            fd.write("\t\theading_level: 1\n")
            fd.write("\t\tshow_root_heading: true\n")
            fd.write("\t\tmembers_order: source\n")

        mkdocs_gen_files.set_edit_path(full_doc_path, Path("../") / path)


def generate_code_section():
    """
    Function for parsing the source folder and registering files in the documentation
    """
    if os.environ.get('STAYA_ECOM_MKDOCS_CODE_PARCE_ENABLED', 't').lower() not in TRUE_CHOICES:
        return

    # parse and register
    source_path = Path(os.environ.get('STAYA_ECOM_MKDOCS_CODE_PARCE_SOURCE_PATH', 'meringue'))
    doc_path = Path(os.environ.get('STAYA_ECOM_MKDOCS_CODE_PARCE_DOCS_PATH', 'reference'))
    nav = mkdocs_gen_files.Nav()
    directory_processing(source_path, doc_path, nav)

    # make navigration
    with mkdocs_gen_files.open(doc_path / "SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())

    # show navigation for debug
    if os.environ.get('STAYA_ECOM_MKDOCS_CODE_PARCE_SHOW_NAV', 'f').lower() in TRUE_CHOICES:
        with mkdocs_gen_files.open(doc_path / "SUMMARY.md", "r") as nav_file:
            print(nav_file.read())


# start generation of docs from code
generate_code_section()
