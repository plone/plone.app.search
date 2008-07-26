from unittest import TestCase
from unittest import makeSuite
from unittest import TestSuite
from plone.app.search.tests.case import IntegrationTestCase
from plone.app.search.utils import quoteSearchString
from plone.app.search.utils import currentCategory
from plone.app.search.utils import objectPathFromSiteRoot
from plone.app.search.utils import brainPathFromSiteRoot

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


class PathToRootTests(IntegrationTestCase):
    def testOneLevelPathToRoot(self):
        obj=self.getObject("/plone/recipes")
        self.assertEqual(self.getPath(obj), "recipes")

    def testTwoLevelPathToRoot(self):
        obj=self.getObject("/plone/recipes/pizza")
        self.assertEqual(self.getPath(obj), "recipes/pizza")


class ObjectPathToRootTests(PathToRootTests):
    def getObject(self, path):
        return self.portal.unrestrictedTraverse(path)

    def getPath(self, obj):
        return objectPathFromSiteRoot(obj)

    def testPathToRoot(self):
        obj=self.getObject("/plone")
        self.assertEqual(self.getPath(obj), "")


class BrainPathToRootTests(PathToRootTests):
    def getObject(self, path):
        hive=self.portal.portal_catalog(path=dict(depth=0, query=path))
        self.assertEqual(len(hive), 1)
        return hive[0]

    def getPath(self, brain):
        return brainPathFromSiteRoot(brain)



def test_suite():
    suite=TestSuite()
    suite.addTest(makeSuite(QuoteSearchStringTests))
    suite.addTest(makeSuite(CurrentCategoryTests))
    suite.addTest(makeSuite(ObjectPathToRootTests))
    suite.addTest(makeSuite(BrainPathToRootTests))
    return suite
