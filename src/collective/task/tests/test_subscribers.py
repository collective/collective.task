from z3c.relationfield.relation import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

from plone import api
from plone.app.testing.interfaces import TEST_USER_NAME

from ecreall.helpers.testing.base import BaseTest

from ..testing import IntegrationTestCase


class TestSubscribers(IntegrationTestCase, BaseTest):
    """Tests subscribers"""

    def setUp(self):
        super(TestSubscribers, self).setUp()
        portal = api.portal.get()
        self.folder = portal['folder']
        self.document = portal['document']
        intids = getUtility(IIntIds)
        self.doc_intid = intids.getId(self.document)

    def test_set_enquirer(self):
        folder = self.folder
        opinion = api.content.create(folder, type="opinion",
                                     id="my-opinion", title="My opinion",
                                     responsible=['bigboss'],
                                     target=RelationValue(self.doc_intid))
        self.assertIn(TEST_USER_NAME, opinion.enquirer)
        validation = api.content.create(folder, type="validation",
                                        id="my-validation", title="My validation",
                                        responsible=['bigboss'],
                                        target=RelationValue(self.doc_intid))
        self.assertIn(TEST_USER_NAME, validation.enquirer)

    def test_set_reader_on_target(self):
        folder = self.folder
        opinion = api.content.create(folder, type="opinion",
                                     id="my-opinion", title="My opinion",
                                     responsible=['miniboss'],
                                     target=RelationValue(self.doc_intid))
        responsible_roles = api.user.get_roles(username='miniboss',
                                               obj=self.document)
        self.assertIn('Reader', responsible_roles)
