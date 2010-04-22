"""This is an integration "unit" test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for 
example.
"""

import unittest
from base import SearchTestCase


class TestBrowser(SearchTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """
    
    def afterSetUp(self):
        """This method is called before each single test. It can be used to
        set up common state. Setup that is specific to a particular test 
        should be done in that test method.
        """
        
    def beforeTearDown(self):
        """This method is called after each single test. It can be used for
        cleanup, if you need it. Note that the test framework will roll back
        the Zope transaction at the end of each test, so tests are generally
        independent of one another. However, if you are modifying external
        resources (say a database) or globals (such as registering a new
        adapter in the Component Architecture during a test), you may want to
        tear things down here.
        """
    
    def test_section(self):
        """Test retrieving section title for search result item."""

        self.setRoles(['Manager', 'Member'])
        
        self.portal.invokeFactory('Document', 'first_level_document')
        self.portal.invokeFactory('Folder', 'first_level_folder', title='First Level Folder')
    
        view = self.portal.restrictedTraverse('@@search')
        
        # return None for first_level objects
        section_title = view.section('http://nohost/plone/first_level_document')
        self.assertEquals(section_title, None)
        
        section_title = view.section('http://nohost/plone/first_level_folder')
        self.assertEquals(section_title, None)
        
        # return section for objects deeper in the hierarchy
        section_title = view.section('http://nohost/plone/first_level_folder/second_level_document')
        self.assertEquals(section_title, 'First Level Folder')
        
        section_title = view.section('http://nohost/plone/first_level_folder/second_level_folder')
        self.assertEquals(section_title, 'First Level Folder')
        
        section_title = view.section('http://nohost/plone/first_level_folder/second_level_folder/third_level_document')
        self.assertEquals(section_title, 'First Level Folder')

    def test_section_cache(self):
        """Test that section title is read from sections_cache dict if an entry already exists."""
        
        self.setRoles(['Manager', 'Member'])
        
        self.portal.invokeFactory('Folder', 'first_level_folder', title='First Level Folder')
        self.portal.first_level_folder.invokeFactory('Document', 'second_level_document')
        
        view = self.portal.restrictedTraverse('@@search')

        # We input an entry for 'first_level_folder' into sections_cache dict and this value should
        # be returned by section() instead of the real title of first_level_folder.
        view.sections_cache['first_level_folder'] = "Cached title for first_level_folder"

        section_title = view.section('http://nohost/plone/first_level_folder/second_level_document')
        self.assertEquals(section_title, 'Cached title for first_level_folder')
        
def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBrowser))
    return suite
