from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.Archetypes.interfaces import IBaseFolder
from Products.CMFPlone.interfaces import INonStructuralFolder
from plone.app.search.utils import addMarkerInterface
from plone.app.search.utils import removeMarkerInterface
from plone.app.search.interfaces import ICategory
from plone.app.search import SearchMessageFactory as _
from archetypes.schemaextender.field import ExtensionField
from Products.Archetypes.atapi import BooleanField
from Products.Archetypes.atapi import BooleanWidget


class InterfaceMarkerField(ExtensionField, BooleanField):
    """Archetypes field to manage marker interface.

    This is a boolean field which will set or unset one or more marker
    interfaces on an object.

    This field can be used with archetypes.schemaextender. It is commonly used
    to manage optional behaviour for existing content types.
    """

    def get(self, instance, **kwargs):
        for iface in self.interfaces:
            if not iface.providedBy(instance):
                return False
        else:
            return True


    def getRaw(self, instance, **kwargs):
        return self.get(instance)


    def set(self, instance, value, **kwargs):
        if value:
            addMarkerInterface(instance, *self.interfaces)
        else:
            removeMarkerInterface(instance, *self.interfaces)


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

