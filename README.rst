====================
collective.task
====================

Tasks management for Plone.

This package provides:

* a new content type called task
* a task behavior, with the same fields as a task
* a fielset task behavior, with the same fields as a task
* a task container behavior, just providing a marker interface

The task behaviour has the following fields:

* a task description: richtext field.
* an assigned group: vocabulary of plone groups (can be redefined). Master field for assigned user
* an assigned user: vocabulary of plone users. Slave field of selected assigned group.
* an enquirer: user proposing the task (authenticated user by default)
* a due date

Assigned group and assigned user are local role fields (dexterity.localrolesfield).
This last product enables to configure (on a dexterity type) the local roles to give (following the workflow state) to the principal selected in object role field.
It's a dynamic local roles assignment.

The task content has the task behaviour and the following fields:

* a title
* parents assigned groups: hidden field. Automatically managed by subscribers.
* parents enquirers: hidden field. Automatically managed by subscribers.

Parents fields contain the values of parents chain corresponding fields (following registry config).
This mechanism allows to give some local roles following parents task assignments.

The default workflow for a task contains the following states:

* created (initial state)
* to assign
* to do
* in progress
* realized
* closed

From the created state, you can choose the transition "to do". There are 2 cases:

* if an assigned user is already selected, an auto transition passes to "to do" state
* if no assigned user is selected, a reviewer must choose one and manually pass to "to do" state

This add-on is tested using Travis CI. The current status of the add-on is :

.. image:: https://secure.travis-ci.org/collective/collective.task.png
    :target: http://travis-ci.org/collective/collective.task
.. image:: https://coveralls.io/repos/collective/collective.task/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/collective/collective.task?branch=master
