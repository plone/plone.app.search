from zope.interface import Interface
from zope.interface import Attribute
from zope.viewlet.interfaces import IViewlet

class ISearchProductLayer(Interface):
    """A skin layer specific for plone.app.search.

    This skin layer will only be present on requests when the plone.app.search
    package is installed in the site.
    """


class ICategory(Interface):
    """Marker interfaces for structural folder that represents a
    category in the site.
    """


class ISearchViewlet(IViewlet):
    """Category-aware search viewlet."""

    category = Attribute("(string) id for the current category, or None "
                         "if not in a category.")

