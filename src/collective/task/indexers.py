from Acquisition import aq_parent
from five import grok
from plone.indexer.decorator import indexer
from Products.CMFCore.utils import getToolByName

from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.container.contained import ContainerModifiedEvent

from collective.dms.basecontent.dmsdocument import IDmsDocument
from collective.task.interfaces import IBaseTask


def get_document(obj):
    parent = obj
    while not IDmsDocument.providedBy(parent):
        parent = aq_parent(parent)
        if parent is None:
            return obj
    return parent

@indexer(IBaseTask)
def enquirer(obj, **kw):
    return obj.enquirer and obj.enquirer[0] or ''


@indexer(IBaseTask)
def responsible(obj, **kw):
    return obj.responsible and obj.responsible[0] or ''


@indexer(IBaseTask)
def deadline(obj, **kw):
    return obj.deadline or obj.modified()


@indexer(IBaseTask)
def document_path(obj, **kw):
    doc = get_document(obj)
    return '/'.join(doc.getPhysicalPath())


@indexer(IBaseTask)
def document_title(obj, **kw):
    doc = get_document(obj)
    return doc.Title()


@grok.subscribe(IDmsDocument, IObjectModifiedEvent)
def reindex_brain_metadata_on_basetask(doc, event):
    if isinstance(event, ContainerModifiedEvent):
        return

    catalog = getToolByName(doc, 'portal_catalog')
    tasks = catalog.unrestrictedSearchResults({
        'object_provides': IBaseTask.__identifier__,
        'path': '/'.join(doc.getPhysicalPath())})
    for b in tasks:
        # reindex id index just to trigger the update of metadata on brain
        b.getObject().reindexObject(idxs=['id'])
