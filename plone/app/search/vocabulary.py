from zope.interface import implements
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName
from plone.app.search.utils import brainPathFromSiteRoot


class CategoryVocabulary(object):
    """Create a vocabulary for categories.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        catalog=getToolByName(context, "portal_catalog")
        url=getToolByName(context, "portal_url")
        categories=catalog(object_provides="plone.app.search.interfaces.ICategory",
                           order_by="sortable_title")

        def createTerm(brain):
            path=brainPathFromSiteRoot(brain)
            return SimpleTerm(path, path, brain.Title)

        return SimpleVocabulary([createTerm(brain) for brain in categories])


CategoryVocabularyFactory = CategoryVocabulary()
