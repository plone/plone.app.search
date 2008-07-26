from Acquisition import aq_chain
from Acquisition import aq_inner
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.search.interfaces import ICategory
from zope.component import getUtility
from zope.app.schema.vocabulary import IVocabularyFactory
from Products.CMFCore.interfaces import ISiteRoot


def currentCategory(context):
    """Return the root of the category for a context.

    If the context object is not inside of a category None is
    returned.
    """
    for entry in aq_chain(aq_inner(context)):
        if ICategory.providedBy(entry):
            return entry
        elif IPloneSiteRoot.providedBy(entry):
            return None
    else:
        return None


def objectPathFromSiteRoot(obj):
    root=getUtility(ISiteRoot)
    rootpath=root.getPhysicalPath()
    objpath=obj.getPhysicalPath()
    return "/".join(objpath[len(rootpath):])


def brainPathFromSiteRoot(brain):
    root=getUtility(ISiteRoot)
    rootpath="/".join(root.getPhysicalPath())
    return brain.getPath()[len(rootpath)+1:]


def quoteSearchString(s):
    """Quote characters in a search string.

    This is needed to prevent text indices from trying to interpret
    unprotected input, which could lead to parsing errors.
    """
    bad_chars = ["(", ")"]
    for char in bad_chars:
        s = s.replace(char, '"%s"' % char)
    return s

