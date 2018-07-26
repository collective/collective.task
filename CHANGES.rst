Changelog
=========

3.1 (unreleased)
----------------

- Corrected table column style. Added contenttype css icon
  [sgeulette]
- pep8 on imports

3.0 (2017-05-30)
----------------

- Modified enquirer field to be LocalRoleField. Use overridable vocabulary.
  [sgeulette]
- Added parents_assigned_groups and parents_enquirers field to manage parents rights
  [sgeulette]
- Block local roles on task content
  [sgeulette]
- Added special index value for empty field.
  [sgeulette]
- Use Owner role in workflow
  [sgeulette]

2.5 (2016-12-07)
----------------

- Set initial_trigger to true.
  [sgeulette]

2.4 (2016-06-22)
----------------

- Add a get_full_tree_title method returning the path title of a task until its parent container.
  [fngaha]


2.3 (2016-04-15)
----------------

- Adapted ITask to add method getting the highest parent.
  [sgeulette]
- Colorize states
  [sgeulette]
- Add icons for transitions
  [sgeulette]
- Add viewlet displaying task parents
  [sgeulette]

2.2.1 (2016-01-13)
------------------

- Modify a copy of the field.
  [sgeulette]

2.2 (2015-11-24)
----------------

- Added TaskContainer related search utility
  [sgeulette]
- Added task content interface to differentiate from behavior
  [sgeulette]
- Added task_description field
  [sgeulette]
- Added assigned_group and due_date indexes. Added indexer methods avoiding acquisition for children. Do not store None in catalog
  [sgeulette]
- Added assigned_group default value. default_value decorator didn't worked.
  Schema defaultFactory is used but is called also in view mode when field is None and can't be less easily overrided !
  [sgeulette]
- Changed workflow to use 'Request review' guard permission to differentiate Reviewer and editor transitions (like in plone workflows)
  [sgeulette]
- Added item_view as default: use simple item view on task content
  [sgeulette]
- Added colorized warning when no assigned user
  [sgeulette]
- Added transition between to_do and realized
  [sgeulette]
- Replaced workflow title ids. Added english translations
  [sgeulette]
- Return unicode in table column
  [sgeulette]

2.1 (2015-06-30)
----------------

- Added uninstall 1.0 profile.
  [sgeulette]
- Corrected bad classifier
  [sgeulette]


2.0 (2015-06-03)
----------------

- Complete refactoring to propose a more generic task content and behaviors.
  [cedricmessiant, sgeulette]


1.0 (2015-03-16)
----------------

- Initial release.
  [cedricmessiant]
