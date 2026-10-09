# make robot, or against a robot server (make robot-server):
#   ZSERVER_PORT=55001 bin/robot-server --no-reload collective.task.testing.COLLECTIVE_TASK_ACCEPTANCE_TESTING
#   ZSERVER_PORT=55001 bin/robot src/collective/task/tests/robot/test_task.robot

*** Settings ***
Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Library  Collections

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Open test browser  AND  Enable autologin as  Manager  AND  the site was rendered once
Test Teardown  Close all browsers


*** Test Cases ***
Scenario: A subtask takes the assigned group of its parent and both views link each other
    Given a task  Parent task  Reviewers
    When I open the add form of a task in  ${PLONE_URL}/parent-task
    Then the assigned group is  Reviewers
    When I save the task  Child task
    Then the page contains a link to  ${PLONE_URL}/parent-task
    When I go to  ${PLONE_URL}/parent-task
    Then the page contains a link to  ${PLONE_URL}/parent-task/child-task

Scenario: The assigned user list follows the assigned group
    When I open the add form of a task in  ${PLONE_URL}
    Then the assigned users are  --NOVALUE--
    When I select the assigned group  Reviewers
    Then the assigned users are  --NOVALUE--  agent
    When I select the assigned user  agent
    And I save the task  Assigned task
    Then the page contains  Agent


*** Keywords ***
the site was rendered once
    [Documentation]  The first page of the test site writes (portlet assignments, imio.helpers volatile
    ...              cache key): plone.protect asks to confirm it once
    Go to  ${PLONE_URL}
    ${confirm}=  Run keyword and return status  Page should contain button  Confirm action
    Run keyword if  ${confirm}  Click button  Confirm action
    Wait until page contains element  css=#content

a task
    [Arguments]  ${title}  ${group}
    I open the add form of a task in  ${PLONE_URL}
    I select the assigned group  ${group}
    I save the task  ${title}

I select the assigned group
    [Arguments]  ${group}
    Select from list by value  css=#form-widgets-ITask-assigned_group  ${group}

I select the assigned user
    [Arguments]  ${user}
    Select from list by value  css=#form-widgets-ITask-assigned_user  ${user}

the assigned users are
    [Documentation]  Option values of the assigned user list, refreshed by masterselect
    [Arguments]  @{users}
    Wait until keyword succeeds  5s  0.5s  List values should be  css=#form-widgets-ITask-assigned_user  @{users}

List values should be
    [Arguments]  ${locator}  @{values}
    ${actual}=  Get list items  ${locator}  values=True
    Lists should be equal  ${actual}  ${values}

the page contains
    [Arguments]  ${text}
    Page should contain  ${text}

I open the add form of a task in
    [Arguments]  ${url}
    Go to  ${url}/++add++task
    Wait until page contains element  css=#form-widgets-title

I save the task
    [Arguments]  ${title}
    Input text  css=#form-widgets-title  ${title}
    Click button  css=#form-buttons-save
    Wait until element contains  css=.portalMessage  Item created

the assigned group is
    [Arguments]  ${group}
    List selection should be  css=#form-widgets-ITask-assigned_group  ${group}

I go to
    [Arguments]  ${url}
    Go to  ${url}

the page contains a link to
    [Arguments]  ${url}
    Page should contain element  css=#content a[href="${url}"]
