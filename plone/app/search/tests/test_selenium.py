from plone.app.search.tests.base import SearchSeleniumTestCase
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD, TEST_USER_ROLES
from plone.app.testing.selenium_layers import open, login


class SimpleScenarioTestCase(SearchSeleniumTestCase):
        
    def test_simple_scenario(self):
        
        portal = self.layer['portal']
        selenium = self.layer['selenium']
        
        # open search form and assert texts
        open(selenium, portal.absolute_url() + '/@@search')
        
        # by default there are no search results
        self.assertEquals(selenium.find_element_by_id('search-results-number').get_text(), '0')
        self.assertEquals(selenium.find_element_by_id('search-results').get_text(), 'No results were found.')
        
        # is search filter hidden?
        self.failUnless('hiddenStructure' in selenium.find_element_by_id('search-filter').get_attribute('class'))
        