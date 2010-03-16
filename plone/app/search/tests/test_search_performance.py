"""This is an integration "unit" test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for 
example.
"""

import unittest
from base import SearchFunctionalTestCase
from Products.CMFCore.utils import getToolByName
from Products.Five.testbrowser import Browser
        

class TestSetup(SearchFunctionalTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """
    
    def afterSetUp(self):
        """This method is called before each single test. It can be used to
        set up common state. Setup that is specific to a particular test 
        should be done in that test method.
        """
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        
    def beforeTearDown(self):
        """This method is called after each single test. It can be used for
        cleanup, if you need it. Note that the test framework will roll back
        the Zope transaction at the end of each test, so tests are generally
        independent of one another. However, if you are modifying external
        resources (say a database) or globals (such as registering a new
        adapter in the Component Architecture during a test), you may want to
        tear things down here.
        """
    
    def test_portal_title(self):
        
        # This is a simple test. The method needs to start with the name
        # 'test'. 

        # Look at the Python unittest documentation to learn more about hte
        # kinds of assertion methods which are available.

        # PloneTestCase has some methods and attributes to help with Plone.
        # Look at the PloneTestCase documentation, but briefly:
        # 
        #   - self.portal is the portal root
        #   - self.folder is the current user's folder
        #   - self.logout() "logs out" so that the user is Anonymous
        #   - self.setRoles(['Manager', 'Member']) adjusts the roles of the current user
        
        self.assertEquals("Plone site", self.portal.getProperty('title'))

    def test_functional_searchresults_page(self):
        """ We make 3 dummy pages, publish them, then check that the rendered search results page 
            says that we got 3 search results. Crude, but useful."""

        self.setRoles(['Manager', 'Member'])
        # make 3 pages, then publish them
        for i in range(0,3):
            new_id = self.folder.invokeFactory('Document', 'my-page'+str(i), text='spam spam ham eggs')
            obj = getattr(self.folder,new_id)
            self.portal.portal_workflow.doActionFor(obj, 'publish')
        # open the search page in the testbrowser
        portal_url = self.portal.absolute_url()
        browser = Browser()
        browser.open(portal_url+'/@@search?SearchableText=spam')
        self.failUnless("3 items matching your search terms" in browser.contents)

    def test_performance_for_100_items(self):
        """
            To make sure we don't make Plone superslower, we run some crude performance tests.
            We make 100 documents, publish them, then search for them. 
            Compare the results with the old search results page
            If we are slower the test fails 
        
            These tests WILL be slow to run. 
            Let's remove or hide these when(if) the PLIP is approved        
        """
        
        print "testing performance with 100 pages"
        from time import time
        self.setRoles(['Manager', 'Member'])
        for i in range(0,100):
            new_id = self.folder.invokeFactory('Document', 'my-page'+str(i), text='spam spam ham eggs')
            obj = getattr(self.folder,new_id)
            self.portal.portal_workflow.doActionFor(obj, 'publish')
        portal_url = self.portal.absolute_url()

        heatup_browser = Browser()
        portal_url = self.portal.absolute_url()
        heatup_browser.open(portal_url+'/search?SearchableText=spam')
        
        # time rendering the old search page
        old_start = time()
        browser = Browser()
        browser.open(portal_url+'/search?SearchableText=spam')
        old_end = time()
        old_time = old_end-old_start
        self.failUnless("100 items matching your search terms" in browser.contents)

        # then time rendering the new search page
        new_start = time()
        browser2 = Browser()
        browser2.open(portal_url+'/@@search?SearchableText=spam')
        new_end = time()
        self.failUnless("100 items matching your search terms" in browser2.contents)

        new_time = new_end-new_start
        print "*" * 20
        print "old search page vs new search page"
        print str(old_time) + " vs " + str(new_time)
        print "*" * 20
        print str((new_time/old_time)*100) + "% time usage"
        self.failUnless((old_time*1.1) >= new_time)


    def test_performance_for_1000_items(self):
        """
            To make sure we don't make Plone superslower, we run some crude performance tests.
            We make 1000 documents, publish them, then search for them. 
            Compare the results with the old search results page
            If we are slower the test fails 
        
            These tests WILL be slow to run. 
            Let's remove or hide these when(if) the PLIP is approved        
        """
        print "testing performance with 1000 pages"
        from time import time
        self.setRoles(['Manager', 'Member'])
        for i in range(0,1000):
            new_id = self.folder.invokeFactory('Document', 'my-page'+str(i), text='spam spam ham eggs')
            obj = getattr(self.folder,new_id)
            self.portal.portal_workflow.doActionFor(obj, 'publish')

        heatup_browser = Browser()
        portal_url = self.portal.absolute_url()
        heatup_browser.open(portal_url+'/search?SearchableText=spam')
        
        # time rendering the old search page
        old_start = time()
        browser = Browser()
        browser.open(portal_url+'/search?SearchableText=spam')
        old_end = time()
        self.failUnless("1000 items matching your search terms" in browser.contents)
        old_time = old_end-old_start

        # then time rendering the new search page
        new_start = time()
        browser2 = Browser()
        browser2.open(portal_url+'/@@search?SearchableText=spam')
        new_end = time()
        self.failUnless("1000 items matching your search terms" in browser2.contents)
        
        new_time = new_end-new_start
        print "*" * 20
        print "old search page vs new search page"
        print str(old_time) + " vs " + str(new_time)
        print "*" * 20
        print str((new_time/old_time)*100) + "% time usage" 
        self.failUnless((old_time*1.1) > new_time, "the new search results page is slower than the old search results page")
        
        

    #  Having tests in multiple files makes
    #  it possible to run tests from just one package:
    #   
    #   ./bin/instance test -s plone.app.search -t test_search_performance


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
