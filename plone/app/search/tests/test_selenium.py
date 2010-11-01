from plone.app.search.tests.base import SearchSeleniumTestCase
from plone.app.testing.selenium_layers import open


class SimpleScenarioTestCase(SearchSeleniumTestCase):
        
    def test_basic_search(self):
        
        portal = self.layer['portal']
        selenium = self.layer['selenium']
        
        # Open search form
        open(selenium, portal.absolute_url() + '/@@search')
        
        # Is search filter hidden?
        self.failUnless('hiddenStructure' in selenium.find_element_by_id('search-filter').get_attribute('class'))
        
        # Is 'relevance' the current/default sorting option and thus 
        # is not clickable?
        sorter = selenium.find_element_by_id('sorting-options')
        self.assertEquals(sorter.find_elements_by_link_text('relevance'), [])
        
        # By default there are no search results because there is no 
        # SearchableText specified in request when accessing the form directly:
        self.assertEquals(selenium.find_element_by_id('search-results-number').get_text(), '0')
        self.assertEquals(selenium.find_element_by_id('search-results').get_text(), 'No results were found.')
        
        # Now we want to get results with all elements in the site:
        open(selenium, portal.absolute_url() + '/@@search?SearchableText=Foo')
        # We should get our 5 'Foo' elements:
        self.assertEquals(selenium.find_element_by_id('search-results-number').get_text(), '5')
        
        