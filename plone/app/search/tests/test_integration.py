import unittest2 as unittest

from DateTime import DateTime

from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import setRoles
from zope.component import getMultiAdapter
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

try:
    from Products.CMFPlone.interfaces import ISearchSchema
    HAS_ISearchSchema = True
except:
    HAS_ISearchSchema = False


from plone.app.contentlisting.interfaces import IContentListing

from base import SearchTestCase, test_request


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
        self.assertEqual(title, None)

        title = crumbs(first_level_folder)
        self.assertEqual(title, None)

        # return section for objects deeper in the hierarchy
        title = crumbs(first_level_folder.second_level_document)[0]['Title']
        self.assertEqual(title, 'First Level Folder')

        title = crumbs(second_level_folder)[0]['Title']
        self.assertEqual(title, 'First Level Folder')

        title = crumbs(second_level_folder.third_level_document)[0]['Title']
        self.assertEqual(title, 'First Level Folder')

    def test_blacklisted_types_in_results(self):
        """Make sure we don't break types' blacklisting in the new search
        results view.
        """
        portal = self.layer['portal']
        registry = getUtility(IRegistry)
        if HAS_ISearchSchema:
            search_settings = registry.forInterface(ISearchSchema,
                                                    prefix="plone")
        else:
            pprops = getToolByName(portal, "portal_properties")
            search_settings = pprops.site_properties

        q = {'SearchableText': 'spam'}
        res = portal.restrictedTraverse('@@search').results(query=q,
                                                            batch=False)
        self.assertTrue('my-page1' in [r.getId() for r in res],
                        'Test document is not found in the results.')

        # Now let's exclude 'Document' from the search results:
        search_settings.types_not_searched = ('Document',)
        res = portal.restrictedTraverse('@@search').results(query=q,
                                                            batch=False)
        self.assertFalse(
            'my-page1' in [r.getId() for r in res],
            'Blacklisted type "Document" has been found in search results.')

    def test_filter_empty(self):
        """Test filtering for empty query"""
        portal = self.layer['portal']
        req = test_request()
        # Search.filter_query() will get SearchableText from form if not
        # passed in explicit query argument:
        req.form['SearchableText'] = 'spam'
        view = getMultiAdapter((portal, req), name=u'search')
        res = view.results(batch=False)
        self.assertTrue('my-page1' in [r.getId() for r in res],
                        'Test document is not found in the results.')
        # filter_query() will return None on invalid query (no real indexes):
        req = test_request()
        req.form['garbanzo'] = 'chickpea'  # just noise, no index for this
        view = getMultiAdapter((portal, req), name=u'search')
        self.assertIsNone(view.filter_query({'b_start': 0, 'b_size': 10}))
        # resulting empty query, ergo no search performed, empty result:
        self.assertFalse(view.results(batch=False))
        # filter_query() succeeds if 1+ real index name added to request:
        req.form['portal_type'] = 'Document'
        self.assertIsNotNone(view.filter_query({'b_start': 0, 'b_size': 10}))
        res = view.results(batch=False)
        self.assertTrue('my-page1' in [r.getId() for r in res],
                        'Test document is not found in the results.')
        # filter_query() also succeeds if 1+ real index name is in the
        # original query:
        req = test_request()
        view = getMultiAdapter((portal, req), name=u'search')
        query = {'portal_type': 'Document'}
        self.assertEqual(view.filter_query(query), query)
        res = view.results(query)
        self.assertTrue('my-page1' in [r.getId() for r in res],
                        'Test document is not found in the results.')

    def test_filter_with_plone3_query(self):
        """Filter should ignore obsolete query parameters, not error. """
        portal = self.layer['portal']
        req = test_request()
        # Search.filter_query() will get SearchableText from form if not
        # passed in explicit query argument:
        req.form['SearchableText'] = 'jobs'
        req.form['Title'] = 'Human resource'
        req.form['Description'] = ''
        req.form['created'] = [DateTime('1970/02/01 00:00:00 GMT+0')]
        req.form['created_usage'] = 'range:min'
        req.form['submit'] = 'Search'
        view = getMultiAdapter((portal, req), name=u'search')
        res = view.results(batch=False)
        self.assertEqual([], [r for r in res])

    def test_default_query(self):
        """Test default_query param (mainly for search view extentions)"""
        portal = self.layer['portal']
        catalog = getToolByName(portal, "portal_catalog")
        req = test_request()

        # 1st: no results
        view = getMultiAdapter((portal, req), name=u'search')
        res = view.results(batch=False)
        self.assertEqual([], [r for r in res])

        # default query for document, we get all the docs by default
        total_docs = len(catalog(portal_type='Document'))
        view.default_query = {'portal_type': 'Document'}
        res = view.results(batch=False)
        self.assertEqual(len(tuple(res)), total_docs)

        # default query for Folders, no results at first
        # because no folder is there
        view.default_query = {'portal_type': 'Folder'}
        res = view.results(batch=False)
        self.assertEqual(len(tuple(res)), 0)

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        for x in xrange(0, 5):
            portal.invokeFactory(
                'Folder',
                'forlder%s' % x,
                title='Folder %s' % x
            )
        total_folders = len(catalog(portal_type='Folder'))
        res = view.results(batch=False)
        self.assertEqual(len(tuple(res)), total_folders)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestIntegration))
    suite.addTest(unittest.makeSuite(TestSection))
    return suite
