from Acquisition import aq_chain
from Acquisition import aq_inner
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.search.interfaces import ICategory


def addMarkerInterface(obj, *ifaces):
    for iface in ifaces:
        if not iface.providedBy(obj):
            alsoProvides(obj, iface)


def removeMarkerInterface(obj, *ifaces):
    for iface in ifaces:
        if iface.providedBy(obj):
            noLongerProvides(obj, iface)


def currentCategory(context):
    for entry in aq_chain(aq_inner(context)):
        if ICategory.providedBy(entry):
            return entry
        elif IPloneSiteRoot.providedBy(entry):
            return None
    else:
        return None


def quoteSearchString(s):
    bad_chars = ["(", ")"]
    for char in bad_chars:
        s = s.replace(char, '"%s"' % char)
    return s

