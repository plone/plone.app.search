from zope.interface import implements
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName


class CategoryVocabulary(object):
    """Create a vocabulary for categories.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        catalog=getToolByName(context, "portal_catalog")
        categories=catalog(object_provides="plone.app.search.interfaces.ICategory")
        return SimpleVocabulary([SimpleTerm(brain.getId, brain.getId, brain.Title)
                                 for brain in categories])


CategoryVocabularyFactory = CategoryVocabulary()
