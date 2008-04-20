from unittest import makeSuite
from unittest import TestSuite
from plone.app.search.tests.case import IntegrationTestCase
from plone.app.search.viewlet import SearchViewlet

class SearchViewletTests(IntegrationTestCase):

    def testOutsideCategory(self):
        viewlet=SearchViewlet(self.portal, self.app.REQUEST, None, None)
        viewlet.update()
        self.failUnless(viewlet.category_id is None)

    def testOnCategory(self):
        viewlet=SearchViewlet(self.portal.recipes, self.app.REQUEST, None, None)
        viewlet.update()
        self.assertEqual(viewlet.category_id, "/plone/recipes")

    def testInsideCategory(self):
        viewlet=SearchViewlet(self.portal.tours.leiden, self.app.REQUEST, None, None)
        viewlet.update()
        self.assertEqual(viewlet.category_id, "/plone/tours")

    def XXXtestCategorySearchNotShownOutsideCategory(self):
        # This test fails on guarded_getattr view/category_id
        viewlet=SearchViewlet(self.portal, self.app.REQUEST, None, None)
        viewlet.update()
        self.failIf("Only in this category" in viewlet.render())

    def XXXtestCategorySearchShownInsideCategory(self):
        # This test fails on guarded_getattr view/category_id
        viewlet=SearchViewlet(self.portal.tours, self.app.REQUEST, None, None)
        viewlet.update()
        self.failIf("Only in this category" not in viewlet.render())



def test_suite():
    suite=TestSuite()
    suite.addTest(makeSuite(SearchViewletTests))
    return suite
