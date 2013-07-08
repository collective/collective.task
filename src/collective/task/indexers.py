from plone.indexer.decorator import indexer

from collective.task.interfaces import IBaseTask


@indexer(IBaseTask)
def enquirer(obj, **kw):
    return obj.enquirer and tuple(obj.enquirer) or ()


@indexer(IBaseTask)
def responsible(obj, **kw):
    return obj.responsible and tuple(obj.responsible) or ()
