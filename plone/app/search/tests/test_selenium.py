from plone.app.search.tests.base import SearchSeleniumTestCase
from plone.app.testing.selenium_layers import open


class SimpleScenarioTestCase(SearchSeleniumTestCase):

    def test_basic_search(self):

        portal = self.layer['portal']
        selenium = self.layer['selenium']

        # Open search form
        open(selenium, portal.absolute_url() + '/@@search')

        # Is search filter hidden?
        f = selenium.find_element_by_id('search-filter')
        self.failUnless('hiddenStructure' in f.get_attribute('class'))

        # Is 'relevance' the current/default sorting option and thus
        # is not clickable?
        sorter = selenium.find_element_by_id('sorting-options')
        self.assertEquals(sorter.find_elements_by_link_text('relevance'), [])

        # By default there are no search results because there is no
        # SearchableText specified in request when accessing the form directly:
        res_num = selenium.find_element_by_id('search-results-number')
        res = selenium.find_element_by_id('search-results')
        self.assertEquals(res_num.get_text(), '0')
        self.assertEquals(res.get_text(), 'No results were found.')

        # Now we want to get results with all elements in the site:
        open(selenium, portal.absolute_url() + '/@@search?SearchableText=Foo')
        # We should get our 5 'Foo' elements:
        res_num = selenium.find_element_by_id('search-results-number')
        self.assertEquals(res_num.get_text(), '5')
        # Filter should still be hidden:
        f = selenium.find_element_by_id('search-filter')
        self.failUnless('hiddenStructure' in f.get_attribute('class'))
