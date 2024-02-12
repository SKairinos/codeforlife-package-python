"""
© Ocado Group
Created on 11/12/2023 at 10:59:40(+00:00).

Setup the Code for Life package during installation. 
"""

import json
import os
import typing as t

from setuptools import find_packages, setup  # type: ignore[import-untyped]

from codeforlife import DATA_DIR, __version__

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

# Walk through data directory and get relative file paths.
data_files, root_dir = [], os.path.dirname(__file__)
for dir_path, dir_names, file_names in os.walk(DATA_DIR):
    rel_data_dir = os.path.relpath(dir_path, root_dir)
    data_files += [
        os.path.join(rel_data_dir, file_name) for file_name in file_names
    ]


def parse_requirements(packages: t.Dict[str, t.Dict[str, t.Any]]):
    """Parse a group of requirements from `Pipfile.lock`.

    https://setuptools.pypa.io/en/latest/userguide/dependency_management.html

    Args:
        packages: The group name of the requirements.

    Returns:
        The requirements as a list of strings, required by `setuptools.setup`.
    """

    requirements: t.List[str] = []
    for name, package in packages.items():
        requirement = name
        if "extras" in package:
            requirement += f"[{','.join(package['extras'])}]"
        if "version" in package:
            requirement += package["version"]
        if "markers" in package:
            requirement += f"; {package['markers']}"
        requirements.append(requirement)

    return requirements


# Parse Pipfile.lock into strings.
with open("Pipfile.lock", "r", encoding="utf-8") as pipfile_lock:
    lock = json.load(pipfile_lock)
    install_requires = parse_requirements(lock["default"])
    dev_requires = parse_requirements(lock["develop"])

setup(
    name="codeforlife",
    version=__version__,
    author="Ocado",
    author_email="code-for-life-full-time-xd@ocado.com",
    description="Code for Life's common code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ocadotechnology/codeforlife-package-python",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    data_files=[(str(DATA_DIR), data_files)],
    package_data={"codeforlife": ["py.typed"]},
    python_requires="==3.8.*",
    install_requires=install_requires,
    extras_require={"dev": dev_requires},
    dependency_links=[],
)
