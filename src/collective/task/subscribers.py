from five import grok

from zope.lifecycleevent.interfaces import IObjectRemovedEvent,\
    IObjectAddedEvent, IObjectModifiedEvent
from zope.container.contained import ContainerModifiedEvent

from plone import api
from Products.DCWorkflow.interfaces import IAfterTransitionEvent

from collective.z3cform.rolefield.field import LocalRolesToPrincipalsDataManager

from collective.task.behaviors import ITarget
from collective.task.content.task import ITask
from collective.task.content.opinion import IOpinion
from collective.task.content.validation import IValidation
from collective.task.interfaces import IBaseTask
from collective.dms.basecontent.dmsdocument import IDmsDocument


def grant_local_role_to_responsible(context, role, target):
    """Grant local role to responsible on target"""
    responsible = context.responsible[0]
    target.manage_addLocalRoles(responsible, [role])
    target.reindexObject()


@grok.subscribe(ITask, IAfterTransitionEvent)
def task_changed_state(context, event):
    """When a task is abandoned or done, check if it is a subtask
    and make the wanted transition to parent
    """
    parent = context.getParentNode()
    if parent.portal_type == 'task':
        with api.env.adopt_roles(['Reviewer']):
            if event.new_state.id == 'done':
                api.content.transition(obj=parent, transition='subtask-done')
                parent.reindexObject(idxs=['review_state'])
            elif event.new_state.id == 'abandoned':
                api.content.transition(obj=parent, transition='subtask-abandoned')
                parent.reindexObject(idxs=['review_state'])


@grok.subscribe(ITask, IObjectRemovedEvent)
def reopen_parent_task(context, event):
    """When a task is deleted, reopen its parent task
    """
    parent = context.getParentNode()
    parent_state = api.content.get_state(parent)
    if parent.portal_type == 'task' and parent_state == 'attributed':
        with api.env.adopt_roles(['Reviewer']):
            api.content.transition(obj=parent, transition='subtask-abandoned')
            parent.reindexObject(idxs=['review_state'])


@grok.subscribe(IBaseTask, IObjectAddedEvent)
def set_enquirer(context, event):
    """Set Enquirer field after task creation"""
    enquirer = api.user.get_current().id
    enquirer_dm = LocalRolesToPrincipalsDataManager(context, IBaseTask['enquirer'])
    enquirer_dm.set((enquirer,))
    context.reindexObject()


@grok.subscribe(ITarget, IObjectAddedEvent)
def set_reader_on_target(context, event):
    """Set Reader role on target to responsible after opinion or validation creation"""
    target = context.target.to_object
    grant_local_role_to_responsible(context, 'Reader', target)


@grok.subscribe(IValidation, IObjectAddedEvent)
def set_reviewer_on_target(context, event):
    """Set Reviewer role on target to responsible after validation creation"""
    target = context.target.to_object
    grant_local_role_to_responsible(context, 'Reviewer', target)


@grok.subscribe(IValidation, IObjectAddedEvent)
@grok.subscribe(IOpinion, IObjectAddedEvent)
def set_contributor_on_document(context, event):
    """Set Contributor role on document to responsible after opinion and
    validation creation. (Contributor can create a new version)
    """
    document = context.getParentNode()
    grant_local_role_to_responsible(context, 'Contributor', document)


@grok.subscribe(IDmsDocument, IObjectModifiedEvent)
def reindex_brain_metadata_on_basetask(doc, event):
    """Reindex brain metadatas when document is modified"""
    if isinstance(event, ContainerModifiedEvent):
        return

    catalog = api.portal.get_tool('portal_catalog')
    tasks = catalog.unrestrictedSearchResults({
        'object_provides': IBaseTask.__identifier__,
        'path': '/'.join(doc.getPhysicalPath())})
    for b in tasks:
        # reindex id index just to trigger the update of metadata on brain
        b._unrestrictedGetObject().reindexObject(idxs=['id'])


@grok.subscribe(IOpinion, IAfterTransitionEvent)
def set_reader_on_versions(context, event):
    """Set Reader role on Opinion enquirer on all versions created by
    the responsible when the Opinion is returned"""
    if event.new_state.id == 'done':
        responsible = context.responsible[0]
        enquirer = context.enquirer[0]
        container_path = '/'.join(context.getParentNode().getPhysicalPath())
        query = {'path': {'query': container_path},
                 'portal_type': 'dmsmainfile',
                 'Creator': responsible}
        catalog = api.portal.get_tool('portal_catalog')
        versions = catalog.searchResults(query)
        for brain in versions:
            version = brain.getObject()
            version.manage_addLocalRoles(enquirer, ['Reader'])
            version.reindexObject()
