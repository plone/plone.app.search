"""This is an integration "unit" test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for 
example.
"""

import unittest2 as unittest
from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import setRoles

from base import SearchTestCase

class TestSection(SearchTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """
    
    def test_section(self):
        """Test retrieving section title for search result item."""
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        
        portal.invokeFactory('Document', 'first_level_document')
        portal.invokeFactory('Folder', 'first_level_folder', title='First Level Folder')
    
        view = portal.restrictedTraverse('@@search')
        
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
        
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        
        portal.invokeFactory('Folder', 'first_level_folder', title='First Level Folder')
        portal.first_level_folder.invokeFactory('Document', 'second_level_document')
        
        view = portal.restrictedTraverse('@@search')

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
    suite.addTest(unittest.makeSuite(TestSection))
    return suite
