from plone.app.search.tests.base import SearchSeleniumTestCase
from plone.app.testing.selenium_layers import open

import time


class SimpleScenarioTestCase(SearchSeleniumTestCase):

    def test_basic_search(self):

        portal = self.layer['portal']
        sel = self.layer['selenium']

        # Open search form
        open(sel, portal.absolute_url() + '/@@search')

        # Is search filter hidden?
        f = sel.find_element_by_id('search-filter')
        self.failUnless('hiddenStructure' in f.get_attribute('class'))

        # Is 'relevance' the current/default sorting option and thus
        # is not clickable?
        sorter = sel.find_element_by_id('sorting-options')
        self.assertEquals(sorter.find_elements_by_link_text('relevance'), [])

        # By default there are no search results because there is no
        # SearchableText specified in request when accessing the form directly:
        res_num = sel.find_element_by_id('search-results-number')
        res = sel.find_element_by_id('search-results')
        self.assertEquals(res_num.get_text(), '0')
        self.assertEquals(res.get_text(), 'No results were found.')

        # Now we want to get results with all elements in the site:
        open(sel, portal.absolute_url() + '/@@search?SearchableText=Foo')
        # We should get our 5 'Foo' elements:
        res_num = sel.find_element_by_id('search-results-number')
        self.assertEquals(res_num.get_text(), '5')
        # Filter should still be hidden:
        f = sel.find_element_by_id('search-filter')
        self.failUnless('hiddenStructure' in f.get_attribute('class'))

        # Make sure we have search results returned after clicking main
        # 'Search' button on the search results form:
        sel.find_elements_by_class_name('searchButton')[1].click()
        # We should give the view some time in order to finish the animation of
        # the search results
        time.sleep(1)
        # And the search results are actually visible, aren't they?:
        self.assert_(sel.find_element_by_id('search-results').is_displayed(),
                     "Search results are not visible.")
