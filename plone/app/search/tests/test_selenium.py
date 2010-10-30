from plone.app.search.tests.base import SearchSeleniumTestCase
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD, TEST_USER_ROLES

class OverlayTestCase(SearchSeleniumTestCase):
        
    def test_simple_search(self):
        
        portal = self.layer['portal']
        selenium = self.layer['selenium']
        
        selenium.get(portal.absolute_url())
        
        # # self.wait()
        # self.selenium.click('link=Log in')
        # self.waitForElement('form#login_form')
        # self.selenium.type("name=__ac_name", TEST_USER_NAME)
        # self.selenium.type("name=__ac_password", TEST_USER_PASSWORD)
        # self.selenium.click("submit")
        # self.wait()
        # self.failUnless(self.selenium.is_text_present("Log out"))