import unittest
import doctest

from Testing import ZopeTestCase as ztc

import base


def test_suite():
    # Wire in integration.txt tests as doctests in the integration layer
    return unittest.TestSuite([
        ztc.ZopeDocFileSuite(
            'tests/functionality.txt', package='plone.app.search',
            test_class=base.SearchFunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        ])
