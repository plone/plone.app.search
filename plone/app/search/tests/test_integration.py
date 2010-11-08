import unittest2 as unittest
from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import setRoles

from Products.CMFCore.utils import getToolByName

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
        portal.invokeFactory('Folder', 'first_level_folder',
                             title='First Level Folder')

        view = portal.restrictedTraverse('@@search')

        # return None for first_level objects
        section_title = \
            view.section('http://nohost/plone/first_level_document')
        self.assertEquals(section_title, None)

        section_title = view.section('http://nohost/plone/first_level_folder')
        self.assertEquals(section_title, None)

        # return section for objects deeper in the hierarchy
        fl_path = 'http://nohost/plone/first_level_folder/'
        section_title = view.section(fl_path + 'second_level_document')
        self.assertEquals(section_title, 'First Level Folder')

        sl_path = fl_path + 'second_level_folder/'
        section_title = view.section(sl_path)
        self.assertEquals(section_title, 'First Level Folder')

        section_title = view.section(sl_path + 'third_level_document')
        self.assertEquals(section_title, 'First Level Folder')

    def test_section_cache(self):
        """Test that section title is read from sections_cache dict if an entry
        already exists.
        """

        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        portal.invokeFactory('Folder', 'first_level_folder',
                             title='First Level Folder')
        portal.first_level_folder.invokeFactory('Document',
                                                'second_level_document')

        view = portal.restrictedTraverse('@@search')

        # We input an entry for 'first_level_folder' into sections_cache dict
        # and this value should be returned by section() instead of the real
        # title of first_level_folder.
        view.sections_cache['first_level_folder'] = \
            "Cached title for first_level_folder"

        fl_path = 'http://nohost/plone/first_level_folder/'
        section_title = view.section(fl_path + 'second_level_document')
        self.assertEquals(section_title, 'Cached title for first_level_folder')

    def test_blacklisted_types_in_results(self):
        """Make sure we don't break types' blacklisting in the new search
        results view.
        """
        portal = self.layer['portal']
        sp = getToolByName(portal, "portal_properties").site_properties
        # not_searched = sp.getProperty('types_not_searched', [])
        q = {'SearchableText': 'spam'}
        res = portal.restrictedTraverse('@@search').results(query=q)
        self.failUnless('my-page1' in [r.getId() for r in res],
                        'Test document is not found in the results.')

        # Now let's exclude 'Document' from the search results:
        # new_blacklist = not_searched + ('Document', )
        # sp.manage_changeProperties(types_not_searched=new_blacklist)
        sp.types_not_searched += ('Document', )
        res = portal.restrictedTraverse('@@search').results(query=q)
        self.failIf('my-page1' in [r.getId() for r in res],
                    'Blacklisted type "Document" has been found in search \
                     results.')


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSection))
    return suite
