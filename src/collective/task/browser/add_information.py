from copy import deepcopy
from z3c.form import button
from zope.i18nmessageid.message import MessageFactory

from plone import api
from plone.dexterity.browser.add import DefaultAddForm
from plone.stringinterp.adapters import _recursiveGetMembersFromIds

from collective.task import _


class AddInformation(DefaultAddForm):
    """Custom add information view"""

    portal_type = "information"

    @button.buttonAndHandler(_('Add'), name='add')
    def handleAdd(self, action):
        portal = api.portal.get()
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        responsible = data['responsible'][0]
        group = api.group.get(responsible)
        if group is not None:
            # responsible is a group, create an Information by user in this group
            groupname = group.getId()
            users = _recursiveGetMembersFromIds(portal, [groupname])
            objs = []
            for user in users:
                username = user.getId()
                _data = deepcopy(data)
                _data['responsible'] = [username]
                obj = self.createAndAdd(_data)
                if obj is not None:
                    objs.append(obj)
            if objs:
                # mark only as finished if we get the new object
                self._finishedAdd = True
        else:
            # responsible is a user
            obj = self.createAndAdd(data)
            if obj is not None:
                # mark only as finished if we get the new object
                self._finishedAdd = True
