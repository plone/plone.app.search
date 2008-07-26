from unittest import makeSuite
from unittest import TestSuite
from plone.app.search.tests.case import IntegrationTestCase
from plone.app.search.vocabulary import CategoryVocabularyFactory

class CategoryVocabularyTests(IntegrationTestCase):
    def testNoCategories(self):
        self.setCategory(self.portal.recipes, False)
        self.setCategory(self.portal.tours, False)
        vocab=CategoryVocabularyFactory(self.portal)
        self.assertEqual(list(vocab), [])

    def testTwoCategories(self):
        self.setCategory(self.portal.recipes, True)
        self.setCategory(self.portal.tours, True)
        vocab=CategoryVocabularyFactory(self.portal)
        self.assertEqual(len(vocab), 2)
        data=[dict(token=term.token, value=term.value, title=term.title)
                        for term in vocab]

        self.assertEqual(data, [
                        dict(token="recipes", value="recipes", title="Recipes"),
                        dict(token="tours", value="tours", title="Tours")])
                


def test_suite():
    suite=TestSuite()
    suite.addTest(makeSuite(CategoryVocabularyTests))
    return suite
