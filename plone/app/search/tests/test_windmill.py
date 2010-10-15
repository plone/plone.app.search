from unittest import TestSuite, makeSuite

from plone.app.search.tests.base import WindmillTestCase


class TestScenario(WindmillTestCase):
    """Testing a scenario that goes through the main functionalities of 
    plone.app.search.
    """

    def test_simple_search(self):
        import pdb; pdb.set_trace( )
        self.wm.open_site(url='/')

    def test_advance_search(self):
        import pdb; pdb.set_trace( )
        self.wm.open_site(url='/')


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestSimpleSearchScenario))
    return suite
