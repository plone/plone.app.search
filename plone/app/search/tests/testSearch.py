from unittest import makeSuite
from unittest import TestSuite
from plone.app.search.tests.case import IntegrationTestCase
from plone.app.search.search import CategorySearchView


class CategorySearchViewTests(IntegrationTestCase):
    def afterSetUp(self):
        super(CategorySearchViewTests, self).afterSetUp()
        self.app.REQUEST["query"]="site"
        self.view=CategorySearchView(self.portal.tours.leiden, self.app.REQUEST)


    def testViewTypes(self):
        self.assertEqual(self.view._viewTypes,
                self.portal.portal_properties.site_properties.typesUseViewActionInListings)


    def testFriendlyTypes(self):
        types=self.view._friendlyTypes
        self.failUnless(isinstance(types, list))


    def testCatalog(self):
        ct=self.view._catalog
        self.assertEqual(ct.__class__.__name__, "CatalogTool")


    def testBrainInfo(self):
        brain=self.portal.portal_catalog(getId="leiden")[0]
        info=self.view._brainInfo(brain)
        self.assertEqual(info["url"], "http://nohost/plone/tours/leiden")
        self.assertEqual(info["author"], "portal_owner")
        self.assertEqual(info["title"], "The best site in the country: Leiden")
        self.failUnless(info["description"].startswith("one two "))
        self.failUnless(info["description"].endswith("..."))
        self.assertEqual(info["review_state"], "private")
        self.assertEqual(info["portal_type"], "document")
        self.assertEqual(info["relevance"], 1)
        self.assertEqual(info["icon_url"], "http://nohost/plone/document_icon.gif")


    def testGetCategoryBrain(self):
        brain=self.view._getCategoryBrain("/plone/tours")
        self.assertEqual(brain.getPath(), "/plone/tours")


    def testGetCategoryBrainWithInvalidPath(self):
        self.assertRaises(IndexError,
                    self.view._getCategoryBrain, "/plone/tours/leiden")


    def testCategories(self):
        categories=[x.getPath() for x in self.view.categories()]
        self.assertEqual(set(categories), set(["/plone/tours", "/plone/recipes"]))


    def testViewVariables(self):
        self.app.REQUEST["category"]="/plone/tours"
        self.view.update()
        self.assertEqual(self.view.query, "site")
        self.assertEqual(self.view.category_id, "/plone/tours")


    def testResultsListCategories(self):
        self.view.update()
        self.failUnless(isinstance(self.view.results, list))
        self.assertEqual(set([c["url"] for c in self.view.results]),
                    set(["http://nohost/plone/tours", "http://nohost/plone/recipes"]))


    def testResultsOnlyListCategoriesWithResults(self):
        self.app.REQUEST["query"]="country"
        self.view.update()
        self.failUnless(isinstance(self.view.results, list))
        self.assertEqual([c["url"] for c in self.view.results],
                         ["http://nohost/plone/tours"])



def test_suite():
    suite=TestSuite()
    suite.addTest(makeSuite(CategorySearchViewTests))
    return suite
