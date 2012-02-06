from selenium.common.exceptions import NoSuchElementException

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
        self.failIf(f.is_displayed())

        # Is 'relevance' the current/default sorting option and thus
        # is not clickable?
        sorter = sel.find_element_by_id('sorting-options')
        self.assertEquals(sorter.find_elements_by_link_text('relevance'), [])

        # By default there are no search results because there is no
        # SearchableText specified in request when accessing the form directly:
        res_num = sel.find_element_by_id('search-results-number')
        res = sel.find_element_by_id('search-results')
        self.assertEquals(res_num.text, '0')
        self.assertEquals(res.text, 'No results were found.')

        # Now we want to get results with all elements in the site.
        # we use the main search form for this search
        content = sel.find_element_by_id('content')
        main_search_form = content.find_element_by_name('searchform')
        search_field = main_search_form.find_element_by_name('SearchableText')
        search_button = main_search_form.find_element_by_css_selector('.searchButton')
        search_field.send_keys('Foo')
        search_button.click()

        # We should give the view some time in order to finish the animation of
        # the search results
        time.sleep(1)

        # We should get our 5 'Foo' elements:
        res_num = sel.find_element_by_id('search-results-number')
        self.assertEquals(res_num.text, '5')
        # Filter should still be hidden:
        f = sel.find_element_by_id('search-filter')
        self.failIf(f.is_displayed())

        # Make sure we have search results returned after clicking main
        # 'Search' button on the search results form:
        sel.find_elements_by_class_name('searchButton')[1].click()
        # We should give the view some time in order to finish the animation of
        # the search results
        time.sleep(1)
        # And the search results are actually visible, aren't they?:
        self.assert_(sel.find_element_by_id('search-results').is_displayed(),
                     "Search results are not visible.")

    def test_relevance_sorting_after_ajax(self):

        """The reason to test this - weird behavior of the link to 'relevance'
           sorting option after some ajax calls.
        """

        # First we test default sorting that should be 'relevance':
        portal = self.layer['portal']
        sel = self.layer['selenium']
        open(sel, portal.absolute_url() + '/@@search?SearchableText=Foo')
        s = sel.find_element_by_id('sorting-options')
        curr = s.find_element_by_tag_name('strong')
        self.assert_('relevance' in curr.text,
                     'Relevance is not default sorting option')

        # Now we try to change sorting and come back to 'relevance' to see that
        # getting back to it highlights the corresponding item # in the sorting
        # bar:
        s.find_element_by_partial_link_text('date').click()
        # At this point we make an ajax call so it's better to wait for it to
        # be finished:
        time.sleep(1)
        curr = s.find_element_by_tag_name('strong')
        self.assert_('date' in curr.text,
                     'Date is not highlighted sorting option after sorting.')

        s.find_element_by_partial_link_text('relevance').click()
        # At this point we make an ajax call so it's better to wait for it to
        # be finished:
        time.sleep(1)
        try:
            curr = s.find_element_by_tag_name('strong')
            self.assert_('relevance' in curr.text,
                         'Relevance is not highlighted sorting option.')
        except NoSuchElementException:
            self.fail("No highlighted element found after ajax call.")

    def test_search_field(self):

        """ We need to make sure links in livesearch are updated and link to
            correct search results view.
        """

        portal = self.layer['portal']
        sel = self.layer['selenium']
        open(sel, portal.absolute_url())
        search_form = sel.find_element_by_id('portal-searchbox')

        # Of course the form is linked to @@search, isn't it?
        form = search_form.find_element_by_name('searchform')
        self.assert_(form.get_attribute('action') ==
                     'http://localhost:55001/plone/@@search')

        search_field = search_form.find_element_by_id('searchGadget')
        search_field.send_keys('wel')
        time.sleep(1)
        # livesearch should be visible now...
        self.assert_(search_form.find_element_by_id('LSResult').is_displayed())
        # ... and we should have at least 2 'Advanced Search' links
        adv = search_form.find_elements_by_partial_link_text('Advanced Search')
        for link in adv:
            href = link.get_attribute('href')
            self.assert_(href == 'http://localhost:55001/plone/@@search')
