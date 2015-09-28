# -*- coding: utf-8 -*-

from plone.app import dexterity
from plone.dexterity.browser.view import DefaultView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class TaskItemView(DefaultView):
    """ Task view using item template for IDexterityContainer """

    index = ViewPageTemplateFile("%s/browser/item.pt" % dexterity.__path__[0])
