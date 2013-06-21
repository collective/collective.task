from zope.interface import implements
from zope import schema

from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.formwidget.datetime.z3cform.widget import DatetimeFieldWidget
from plone.supermodel import model

from collective.z3cform.rolefield.field import LocalRolesToPrincipals

from collective.task import _


class ITask(model.Schema):
    """Schema for task"""
    title = schema.TextLine(title=_(u'Title'))
    deadline = schema.Datetime(title=_(u'Deadline'),
                               required=False)
    form.widget(deadline=DatetimeFieldWidget)

    responsible = LocalRolesToPrincipals(
        title=_(u"Responsible"),
        roles_to_assign=('Editor',),
        value_type=schema.Choice(
            vocabulary="plone.principalsource.Principals"
        ),
        min_length=1,
        max_length=1,
        required=True,
    )


class Task(Container):
    """Task content type"""
    implements(ITask)

    meta_type = 'task'
    # disable local roles inheritance
    __ac_local_roles_block__ = True
