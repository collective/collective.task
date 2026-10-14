"""Installer for the collective.task package."""

from setuptools import setup

long_description = (
    open("README.rst").read() + "\n" + "Contributors\n"
    "============\n"
    + "\n"
    + open("CONTRIBUTORS.rst").read()
    + "\n"
    + open("CHANGES.rst").read()
    + "\n"
)


setup(
    name="collective.task",
    version="4.0.0.dev0",
    description="Tasks management for Plone.",
    long_description=long_description,
    # Get more from https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Framework :: Plone :: 6.2",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    keywords="Plone Python",
    author="Cedric Messiant",
    author_email="cedricmessiant@ecreall.com",
    url="https://github.com/collective/collective.task",
    download_url="https://pypi.org/project/collective.task",
    license="GPL",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "collective.z3cform.datagridfield",
        "dexterity.localroles>=2.0.0a0",
        "dexterity.localrolesfield>=2.0.0a0",
        "imio.helpers>=1.0.0rc2",
        "imio.migrator",
        "plone.api",
        "plone.app.dexterity",
        "plone.app.layout",
        "plone.app.lockingbehavior",
        "plone.app.textfield",
        "plone.autoform",
        "plone.base",
        "plone.behavior",
        "plone.dexterity",
        "plone.formwidget.masterselect",
        "plone.indexer",
        "plone.registry",
        "plone.supermodel",
        "Products.CMFCore",
        "Products.CMFPlone",
        "Products.DCWorkflow",
        "Products.GenericSetup",
        "z3c.form",
        "z3c.table>=2.2",
        "Zope",
    ],
    extras_require={
        "test": [
            "collective.eeafaceted.batchactions",
            "imio.prettylink",
            "plone.app.robotframework[debug]",
            "plone.app.testing",
            "plone.browserlayer",
            "plone.testing",
            "robotsuite",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
