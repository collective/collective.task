# -*- coding: utf-8 -*-

from plone.indexer import indexer
from Products.CMFCore.interfaces import IContentish
from Products.CMFPlone.utils import base_hasattr
from Products.PluginIndexes.common.UnIndex import _marker as common_marker
from Products.PluginIndexes.DateIndex.DateIndex import _marker as date_marker


@indexer(IContentish)
def assigned_user_index(obj):
    """ Index method escaping acquisition """
    if base_hasattr(obj, 'assigned_user'):
        return obj.assigned_user
    return common_marker


@indexer(IContentish)
def due_date_index(obj):
    """ Index method escaping acquisition """
    if base_hasattr(obj, 'due_date'):
        return obj.due_date
    return date_marker
