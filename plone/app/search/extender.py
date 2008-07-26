from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.Archetypes.interfaces import IBaseFolder
from Products.Archetypes.atapi import BooleanWidget
from Products.CMFPlone.interfaces import INonStructuralFolder
from plone.app.search.interfaces import ICategory
from plone.app.search import SearchMessageFactory as _
from archetypes.markerfield import InterfaceMarkerField


class FolderExtender(object):
    """Add a new 'category' field to all Archetypes based folder types.
    """
    adapts(IBaseFolder)
    implements(ISchemaExtender)

    fields = [
            InterfaceMarkerField("category",
                schemata = "settings",
                interfaces = (ICategory,),
                widget = BooleanWidget(
                    title = _(u"label_category",
                                default=u"Is this folder a category."),
                    description = _(u"help_category",
                                default=u"This should briefly explain what "
                                        u"categories are used for."),
                    ),
                ),
            ]


    def __init__(self, context):
        self.context = context


    def getFields(self):
        if INonStructuralFolder.providedBy(self.context):
            return []

        return self.fields

