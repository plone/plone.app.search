import unittest2 as unittest
from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import setRoles

from plone.app.contentlisting.interfaces import IContentListing
from Products.CMFCore.utils import getToolByName

from base import SearchTestCase


class TestIntegration(SearchTestCase):
    """ Check that all bits of the package are inplace and work.
    """

    def test_searchjs_is_available(self):
        """Make sure search.js is available."""
        portal = self.layer['portal']
        js = getToolByName(portal, 'portal_javascripts')
        ids = js.getResourcesDict().keys()
        self.assert_('++resource++search.js' in ids)


class TestSection(SearchTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """

    def test_breadcrumbs(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        portal.invokeFactory('Document', 'first_level_document')
        portal.invokeFactory('Folder', 'first_level_folder',
                             title='First Level Folder')
        first_level_folder = portal.first_level_folder
        first_level_folder.invokeFactory('Document', 'second_level_document')
        first_level_folder.invokeFactory('Folder', 'second_level_folder')
        second_level_folder = first_level_folder.second_level_folder
        second_level_folder.invokeFactory('Document', 'third_level_document')

        view = portal.restrictedTraverse('@@search')

        def crumbs(item):
            return view.breadcrumbs(IContentListing([item])[0])

        # return None for first_level objects
        title = crumbs(portal.first_level_document)
        self.assertEquals(title, None)

        title = crumbs(first_level_folder)
        self.assertEquals(title, None)

        # return section for objects deeper in the hierarchy
        title = crumbs(first_level_folder.second_level_document)[0]['Title']
        self.assertEquals(title, 'First Level Folder')

        title = crumbs(second_level_folder)[0]['Title']
        self.assertEquals(title, 'First Level Folder')

        title = crumbs(second_level_folder.third_level_document)[0]['Title']
        self.assertEquals(title, 'First Level Folder')

    def test_blacklisted_types_in_results(self):
        """Make sure we don't break types' blacklisting in the new search
        results view.
        """
        portal = self.layer['portal']
        sp = getToolByName(portal, "portal_properties").site_properties
        q = {'SearchableText': 'spam'}
        res = portal.restrictedTraverse('@@search').results(query=q,
                                                            batch=False)
        self.failUnless('my-page1' in [r.getId() for r in res],
                        'Test document is not found in the results.')

        # Now let's exclude 'Document' from the search results:
        sp.types_not_searched += ('Document', )
        res = portal.restrictedTraverse('@@search').results(query=q,
                                                            batch=False)
        self.failIf('my-page1' in [r.getId() for r in res],
                    'Blacklisted type "Document" has been found in search \
                     results.')


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestIntegration))
    suite.addTest(unittest.makeSuite(TestSection))
    return suite
