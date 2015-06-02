====================
collective.task
====================

Tasks management for Plone.

This package provides:

* a new content type called task
* a task behavior, with the same fields as a task
* a fielset task behavior, with the same fields as a task
* a task container behavior, just providing a marker interface

A task has the following fields:

* an assigned group: vocabulary of plone groups (can be redefined). Master field for assigned user
* an assigned user: vocabulary of plone users. Slave field of selected assigned group.
* an enquirer: user proposing the task (authenticated user by default)
* a due date

Assigned group and assigned user are local role fields (dexterity.localrolesfield).
This last product permits to configure (on a dexterity type) the local roles to give on each workflow state, to the selected principal of each role field on the object.

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
