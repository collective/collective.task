from Acquisition import aq_parent
from five import grok

from plone import api
from plone.indexer.decorator import indexer
from Products.CMFCore.utils import getToolByName

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
