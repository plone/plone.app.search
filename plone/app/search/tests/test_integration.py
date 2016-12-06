import unittest2 as unittest

from DateTime import DateTime

from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import setRoles
from zope.component import getMultiAdapter

from plone.app.contentlisting.interfaces import IContentListing
from Products.CMFCore.utils import getToolByName

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

    def test_default_search_order_relevance(self):
        """Test default order as relevance."""
        portal = self.layer['portal']
        sp = getToolByName(portal, 'portal_properties').site_properties
        self.assertEqual(sp.sort_on, 'relevance')

        q = {'SearchableText': 'spam'}
        res = portal.restrictedTraverse('@@search').results(query=q)
        ids = [r.getId() for r in res]
        expected = [
            'my-page11', 'my-page10', 'my-page9', 'my-page8', 'my-page7',
            'my-page6', 'my-page5', 'my-page4', 'my-page3', 'my-page2'
        ]
        self.assertEqual(ids, expected)

    def test_default_search_order_date(self):
        """Test default order as date."""
        portal = self.layer['portal']

        # Change one object date to see if order change works
        mp5 = portal['my-page5']
        mp5.setEffectiveDate(DateTime() + 1)
        mp5.reindexObject()

        sp = getToolByName(portal, 'portal_properties').site_properties
        sp.sort_on = 'Date'
        q = {'SearchableText': 'spam'}
        res = portal.restrictedTraverse('@@search').results(query=q)
        ids = [r.getId() for r in res]
        expected = [
            'my-page11', 'my-page10', 'my-page9', 'my-page8', 'my-page7',
            'my-page6', 'my-page4', 'my-page3', 'my-page2', 'my-page1'
        ]
        self.assertEqual(ids, expected)

    def test_default_search_order_alphabetic(self):
        """Test default order as alphabetic."""
        portal = self.layer['portal']

        sp = getToolByName(portal, 'portal_properties').site_properties
        sp.sort_on = 'sortable_title'
        q = {'SearchableText': 'spam'}
        res = portal.restrictedTraverse('@@search').results(query=q)
        ids = [r.getId() for r in res]
        expected = [
            'my-page0', 'my-page1', 'my-page2', 'my-page3', 'my-page4',
            'my-page5', 'my-page6', 'my-page7', 'my-page8', 'my-page9'
        ]
        self.assertEqual(ids, expected)

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

    def test_filter_empty(self):
        """Test filtering for empty query"""
        portal = self.layer['portal']
        req = test_request()
        # Search.filter_query() will get SearchableText from form if not
        # passed in explicit query argument:
        req.form['SearchableText'] = 'spam'
        view = getMultiAdapter((portal, req), name=u'search')
        res = view.results(batch=False)
        result_ids = [r.getId() for r in res]
        self.failUnless('my-page1' in result_ids,
                        'Test document is not found in the results: %r.' %
                        result_ids)
        # filter_query() will return None on invalid query (no real indexes):
        req = test_request()
        req.form['garbanzo'] = 'chickpea'  # just noise, no index for this
        view = getMultiAdapter((portal, req), name=u'search')
        self.assertIsNone(view.filter_query({'b_start':0, 'b_size':10}))
        # resulting empty query, ergo no search performed, empty result:
        self.assertFalse(view.results(batch=False))
        # filter_query() succeeds if 1+ real index name added to request:
        req.form['portal_type'] = 'Document'
        self.assertIsNotNone(view.filter_query({'b_start':0, 'b_size':10}))
        res = view.results(batch=False)
        result_ids = [r.getId() for r in res]
        self.failUnless('my-page1' in result_ids,
                        'Test document is not found in the results: %r.' %
                        result_ids)
        # filter_query() also succeeds if 1+ real index name is in the original query:
        req = test_request()
        view = getMultiAdapter((portal, req), name=u'search')
        query = {'portal_type': 'Document'}
        self.assertEqual(view.filter_query(query), query)
        res = view.results(query, batch=False)
        result_ids = [r.getId() for r in res]
        self.failUnless('my-page1' in result_ids,
                        'Test document is not found in the results: %r' %
                        result_ids)

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

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestIntegration))
    suite.addTest(unittest.makeSuite(TestSection))
    return suite
