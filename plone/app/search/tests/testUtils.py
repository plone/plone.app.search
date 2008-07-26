from unittest import TestCase
from unittest import makeSuite
from unittest import TestSuite
from plone.app.search.tests.case import IntegrationTestCase
from plone.app.search.utils import quoteSearchString
from plone.app.search.utils import currentCategory

class QuoteSearchStringTests(TestCase):
    def testEmptyString(self):
        self.assertEqual(quoteSearchString(""), "")


    def testCorrectString(self):
        self.assertEqual(quoteSearchString("this is fine"), "this is fine")


    def testSingleBadChar(self):
        self.assertEqual(quoteSearchString("( is bad"), '"(" is bad')


    def testMultipleBadChars(self):
        self.assertEqual(quoteSearchString("( and ) are bad"),
                         '"(" and ")" are bad')



class CurrentCategoryTests(IntegrationTestCase):
    def testSiteRootIsNoCategory(self):
        self.failUnless(currentCategory(self.portal) is None)


    def testCategoryIsInItself(self):
        recipes=self.portal.recipes
        self.failUnless(currentCategory(recipes) is recipes)


    def testItemInsideCategory(self):
        recipes=self.portal.recipes
        self.failUnless(currentCategory(recipes.pizza) is recipes)



def test_suite():
    suite=TestSuite()
    suite.addTest(makeSuite(QuoteSearchStringTests))
    suite.addTest(makeSuite(CurrentCategoryTests))
    return suite
