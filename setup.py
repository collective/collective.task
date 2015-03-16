# -*- coding: utf-8 -*-
"""Installer for the collective.task package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')


setup(
    name='collective.task',
    version='2.0.dev0',
    description="Task management for plone",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='tasks,task,plone',
    author='Cédric Messiant',
    author_email='cedricmessiant@ecreall.com',
    url='http://pypi.python.org/pypi/collective.task',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.dms.basecontent',
        'collective.z3cform.chosen',
        'collective.z3cform.rolefield',
        'five.grok',
        'plone.api',
        'plone.app.dexterity',
        'plone.app.relationfield',
        'plone.directives.form',
        'plone.formwidget.datetime',
        'plone.principalsource',
        'setuptools',
    ],
    extras_require={
        'test': [
            'ecreall.helpers.testing',
            'plone.app.testing',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
