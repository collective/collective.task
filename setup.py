# -*- coding: utf-8 -*-
"""Installer for the collective.task package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open("README.rst").read() + "\n" + "Contributors\n"
    "============\n" + "\n" + open("CONTRIBUTORS.rst").read() + "\n" + open("CHANGES.rst").read() + "\n"
)


setup(
    name="collective.task",
    version="3.0.13.dev0",
    description="Tasks management for Plone.",
    long_description=long_description,
    # Get more from https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="Plone Python",
    author="Cedric Messiant",
    author_email="cedricmessiant@ecreall.com",
    url="https://github.com/collective/collective.task",
    download_url="https://pypi.org/project/collective.task",
    license="GPL",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "dexterity.localroles>=2.0.0a0",
        "dexterity.localrolesfield>=2.0.0a0",
        "plone.api",
        "plone.app.lockingbehavior",
        "plone.formwidget.masterselect",
        'plone.principalsource; python_version<"3"',
        "future",
        "imio.helpers>=1.0.0rc2",
        "imio.migrator",
        "setuptools",
        "z3c.table>=2.2",
    ],
    extras_require={
        "test": [
            "collective.eeafaceted.batchactions",
            "imio.prettylink",
            "plone.app.testing",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
