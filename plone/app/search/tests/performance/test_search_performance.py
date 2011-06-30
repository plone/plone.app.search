import unittest2 as unittest
from plone.app.search.tests.base import Search100FunctionalTestCase, \
                                        Search1000FunctionalTestCase
from plone.testing.z2 import Browser


class TestPerformance100(Search100FunctionalTestCase):

    def setUp(self):
        """This method is called before each single test. It can be used to
        set up common state. Setup that is specific to a particular test
        should be done in that test method.
        """
        # super(TestSetup, self).setUp()
        # self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.portal = self.layer['portal']
        self.app = self.layer['app']

    def test_performance_for_100_items(self):
        """
            To make sure we don't make Plone superslower, we run some crude
            performance tests. We make 100 documents, publish them, then search
            for them. Compare the results with the old search results page If
            we are slower the test fails.
        """
        from time import time

        heatup_browser = Browser(self.app)
        portal_url = self.portal.absolute_url()
        heatup_browser.open(portal_url+'/search?SearchableText=spam')
        heatup_browser.open(portal_url+'/@@search?SearchableText=spam')

        # time rendering the old search page
        browser = Browser(self.app)
        old_start = time()
        browser.open(portal_url+'/search?SearchableText=spam')
        old_end = time()
        old_time = old_end-old_start
        self.assertTrue('100 items matching your search terms' \
                        in browser.contents)

        # then time rendering the new search page
        browser2 = Browser(self.app)
        new_start = time()
        browser2.open(portal_url+'/@@search?SearchableText=spam')
        new_end = time()
        self.assertTrue('<strong id="search-results-number">100</strong>' \
                        in browser2.contents)

        new_time = new_end-new_start
        print "*" * 20
        print "old search page vs new search page"
        print str(old_time) + " vs " + str(new_time)
        print "*" * 20
        self.failUnless(old_time >= new_time,
                        "the new search results page is slower than the old \
                         search results page")


class TestPerformance1000(Search1000FunctionalTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """

    def setUp(self):
        """This method is called before each single test. It can be used to
        set up common state. Setup that is specific to a particular test
        should be done in that test method.
        """
        # super(TestSetup, self).setUp()
        # self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.portal = self.layer['portal']
        self.app = self.layer['app']

    def test_performance_for_1000_items(self):
        """
            To make sure we don't make Plone superslower, we run some crude
            performance tests. We make 1000 documents, publish them, then
            search for them. Compare the results with the old search results
            page If we are slower the test fails.

            These tests WILL be slow to run.
            Let's remove or hide these when(if) the PLIP is approved
        """

        from time import time

        heatup_browser = Browser(self.app)
        portal_url = self.portal.absolute_url()
        heatup_browser.open(portal_url+'/search?SearchableText=spam')
        heatup_browser.open(portal_url+'/@@search?SearchableText=spam')

        # time rendering the old search page
        browser = Browser(self.app)
        old_start = time()
        browser.open(portal_url+'/search?SearchableText=spam')
        old_end = time()
        self.assertTrue('1000 items matching your search terms' \
                        in browser.contents)
        old_time = old_end-old_start

        # then time rendering the new search page
        browser2 = Browser(self.app)
        new_start = time()
        browser2.open(portal_url+'/@@search?SearchableText=spam')
        new_end = time()
        self.assertTrue('<strong id="search-results-number">1000</strong>' \
                        in browser2.contents)

        new_time = new_end-new_start
        print "*" * 20
        print "old search page vs new search page"
        print str(old_time) + " vs " + str(new_time)
        print "*" * 20
        self.failUnless(old_time > new_time,
                        "the new search results page is slower than the old \
                         search results page")


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPerformance100))
    suite.addTest(unittest.makeSuite(TestPerformance1000))
    return suite
