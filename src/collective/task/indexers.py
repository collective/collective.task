from plone.indexer.decorator import indexer

from collective.task.interfaces import IBaseTask


@indexer(IBaseTask)
def enquirer(obj, **kw):
    return obj.enquirer[0]


@indexer(IBaseTask)
def responsible(obj, **kw):
    return obj.responsible[0]
