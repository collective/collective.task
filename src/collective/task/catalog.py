from copy import copy

from App.special_dtml import DTMLFile
from zope.component.hooks import getSite

from Products.PluginIndexes.KeywordIndex.KeywordIndex import KeywordIndex
from Products.CMFCore.utils import getToolByName


def all_principals_for_users(site, users):
    groups_and_users = set([])
    mtool = getToolByName(site, 'portal_membership')
    for user_id in users:
        groups_and_users.add(user_id)
        user = mtool.getMemberById(user_id)
        if hasattr(user, 'getGroups'):
            groups_and_users |= set(user.getGroups())

    return list(groups_and_users)


class UsersAndGroupsIndex(KeywordIndex):
    meta_type="UsersAndGroupsIndex"

    def _apply_index(self, request, *args, **kwargs):
        request = copy(request)
        key = request.keys()[0]
        value = request[key]
        if isinstance(value, basestring):
            value = [value]

        site = getSite()
        request[key] = all_principals_for_users(site, value)
        return super(UsersAndGroupsIndex, self)._apply_index(request, *args, **kwargs)


def manage_addUsersAndGroupsIndex(self, id, extra=None,
        REQUEST=None, RESPONSE=None, URL3=None):
    """Add a keyword index"""
    return self.manage_addIndex(id, 'UsersAndGroupsIndex', extra=extra, \
              REQUEST=REQUEST, RESPONSE=RESPONSE, URL1=URL3)

manage_addUsersAndGroupsIndexForm = DTMLFile('dtml/addUsersAndGroupsIndex', globals())
