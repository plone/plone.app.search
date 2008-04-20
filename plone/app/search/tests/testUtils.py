from zope.interface import Interface
from zope.interface import implements
from zope.interface import providedBy
from unittest import TestCase
from unittest import makeSuite
from unittest import TestSuite
from plone.app.search.tests.case import IntegrationTestCase
from plone.app.search.utils import addMarkerInterface
from plone.app.search.utils import removeMarkerInterface
from plone.app.search.utils import quoteSearchString
from plone.app.search.utils import currentCategory
from plone.app.search.interfaces import ICategory

class MarkerInterface(Interface):
    pass

class SecondMarkerInterface(Interface):
    pass

class BaseInterface(Interface):
    pass

class Mock(object):
    pass

class MockWithInterface(object):
    implements(BaseInterface)
    

class InterfaceTests(TestCase):
    def ifaces(self, obj):
        return [i.getName() for i in providedBy(obj)]


    def testAddNothing(self):
        obj=Mock()
        addMarkerInterface(obj)
        self.assertEqual(self.ifaces(obj), [])


    def testAddSingleInterface(self):
        obj=Mock()
        addMarkerInterface(obj, MarkerInterface)
        self.assertEqual(self.ifaces(obj), ["MarkerInterface"])


    def testAddMultipleInterfaces(self):
        obj=Mock()
        addMarkerInterface(obj, MarkerInterface, SecondMarkerInterface)
        self.assertEqual(self.ifaces(obj),
                         ["MarkerInterface", "SecondMarkerInterface"])


    def testAddAdditionalInterface(self):
        obj=MockWithInterface()
        addMarkerInterface(obj, MarkerInterface)
        self.assertEqual(self.ifaces(obj), ["MarkerInterface", "BaseInterface"])


    def testRemoveNonPresentInterface(self):
        obj=Mock()
        removeMarkerInterface(obj, MarkerInterface)
        self.assertEqual(self.ifaces(obj), [])


    def testAddAndRemoveSingleInterface(self):
        obj=Mock()
        addMarkerInterface(obj, MarkerInterface)
        removeMarkerInterface(obj, MarkerInterface)
        self.assertEqual(self.ifaces(obj), [])


    def testAddTwoInterfacesAndRemoveOne(self):
        obj=Mock()
        addMarkerInterface(obj, MarkerInterface, SecondMarkerInterface)
        removeMarkerInterface(obj, MarkerInterface)
        self.assertEqual(self.ifaces(obj), ["SecondMarkerInterface"])



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
    suite.addTest(makeSuite(InterfaceTests))
    suite.addTest(makeSuite(QuoteSearchStringTests))
    suite.addTest(makeSuite(CurrentCategoryTests))
    return suite
