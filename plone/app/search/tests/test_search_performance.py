"""This is an integration "unit" test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for 
example.
"""

import unittest
from base import SearchTestCase, SearchFunctionalTestCase
from Products.CMFCore.utils import getToolByName
from zope.interface.verify import verifyObject 
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
        # we need to make sure that we don't make Plone superslower.
        # in this test, we make 100 documents, then search for them 
        # first in the old search form
        # then in the new search form
        # we time the results and compare them. 
        # if the new result is slower than the old, the test fails
        
        from time import time
        self.setRoles(['Manager', 'Member'])
        #make 10 pages
        for i in range(0,10):
            new_id = self.folder.invokeFactory('Document', 'my-page'+str(i), text='spam spam ham eggs')
            obj = getattr(self.folder,new_id)
            self.portal.portal_workflow.doActionFor(obj, 'publish')
        portal_url = self.portal.absolute_url()
        browser2 = Browser()
        browser2.open(portal_url+'/@@search?SearchableText=spam')
        self.failUnless("10 items matching your search terms" in browser2.contents)

    def test_performance_for_100_items(self):
        # we need to make sure that we don't make Plone superslower.
        # in this test, we make 100 documents, then search for them 
        # first in the old search form
        # then in the new search form
        # we time the results and compare them. 
        # if the new result is slower than the old, the test fails
        print "testing preformance with 100 pages"
        from time import time
        self.setRoles(['Manager', 'Member'])
        for i in range(0,100):
            new_id = self.folder.invokeFactory('Document', 'my-page'+str(i), text='spam spam ham eggs')
            obj = getattr(self.folder,new_id)
            self.portal.portal_workflow.doActionFor(obj, 'publish')
        portal_url = self.portal.absolute_url()
        
        # time rendering the old search page
        old_start = time()
        browser = Browser()
        browser.open(portal_url+'/search?SearchableText=spam')
        old_end = time()
        old_time = old_end-old_start

        # then time rendering the new search page
        new_start = time()
        browser2 = Browser()
        browser2.open(portal_url+'/@@search?SearchableText=spam')
        new_end = time()
        new_time = new_end-new_start
        print str(old_time) + " vs " + str(new_time)
        print "*" * 20
        self.failUnless(old_time > new_time)


    def test_performance_for_1000_items(self):
        # we need to make sure that we don't make Plone superslower.
        # in this test, we make 100 documents, then search for them 
        # first in the old search form
        # then in the new search form
        # we time the results and compare them. 
        # if the new result is slower than the old, the test fails
        
        print "testing preformance with 1000 pages"
        from time import time
        self.setRoles(['Manager', 'Member'])
        for i in range(0,1000):
            new_id = self.folder.invokeFactory('Document', 'my-page'+str(i), text='spam spam ham eggs')
            obj = getattr(self.folder,new_id)
            self.portal.portal_workflow.doActionFor(obj, 'publish')
        portal_url = self.portal.absolute_url()
        
        # time rendering the old search page
        old_start = time()
        browser = Browser()
        browser.open(portal_url+'/search?SearchableText=spam')
        old_end = time()
        old_time = old_end-old_start

        # then time rendering the new search page
        new_start = time()
        browser2 = Browser()
        browser2.open(portal_url+'/@@search?SearchableText=spam')
        new_end = time()
        new_time = new_end-new_start
        print "1000 items"
        print str(old_time) + " vs " + str(new_time)
        print "*" * 20
        self.failUnless(old_time > new_time, "the new search results page is slower than the old search results page")


    
    

    #  Having tests in multiple files makes
    #  it possible to run tests from just one package:
    #   
    #   ./bin/instance test -s example.tests -t test_integration_unit


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
