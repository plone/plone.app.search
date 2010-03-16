"""This is an integration "unit" test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for 
example.
"""

import unittest
from base import SearchTestCase
from plone.app.search.browser import Search        

class TestBrowser(SearchTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """
    
    def afterSetUp(self):
        """This method is called before each single test. It can be used to
        set up common state. Setup that is specific to a particular test 
        should be done in that test method.
        """
        
    def beforeTearDown(self):
        """This method is called after each single test. It can be used for
        cleanup, if you need it. Note that the test framework will roll back
        the Zope transaction at the end of each test, so tests are generally
        independent of one another. However, if you are modifying external
        resources (say a database) or globals (such as registering a new
        adapter in the Component Architecture during a test), you may want to
        tear things down here.
        """
    
    def test_truncate_url(self):
        """Test url truncating."""
   
        # Don't do anything with short URLs.
        self.assertEquals(Search.truncate_url('http://domain.com'), 'http://domain.com')
        
        # Truncate too long path
        original_url = 'http://domain.com/first-level/second/level/some-file'
        truncated_url = 'http://domain.com/&hellip;/some-file'
        self.assertEquals(Search.truncate_url(original_url, url_threshold=10), truncated_url)
        
        # Truncate too long filename
        original_url = 'http://domain.com/first-level/second/level/more-than-10-characters'
        truncated_url = 'http://domain.com/&hellip;/more-than-&hellip;'
        self.assertEquals(Search.truncate_url(original_url, url_threshold=10, filename_threshold=10), truncated_url)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBrowser))
    return suite
