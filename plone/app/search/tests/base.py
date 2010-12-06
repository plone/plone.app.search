import unittest2 as unittest

from zope.configuration import xmlconfig

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing.selenium_layers import SELENIUM_PLONE_FUNCTIONAL_TESTING


class SearchLayer(PloneSandboxLayer):
    """Install plone.app.search"""

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import plone.app.contentlisting
        import plone.app.search
        xmlconfig.file('configure.zcml',
                       plone.app.contentlisting, context=configurationContext)
        xmlconfig.file('configure.zcml',
                       plone.app.search, context=configurationContext)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'plone.app.search:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        for i in range(0, 100):
            portal.invokeFactory('Document',
                                 'my-page'+str(i),
                                 text='spam spam ham eggs')
        setRoles(portal, TEST_USER_ID, ['Member'])

        # Commit so that the test browser sees these objects
        import transaction
        transaction.commit()


class SearchSeleniumLayer(SearchLayer):
    """Install plone.app.search"""

    defaultBases = (PLONE_FIXTURE, )

    def setUpPloneSite(self, portal):
        """Add content we can search for."""
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Document', 'document1', title='Foo Document 1')
        portal.invokeFactory('Folder', 'folder1', title='Foo Folder 1')
        portal.folder1.invokeFactory('Event', 'event1', title='Foo Event 1')
        portal.folder1.invokeFactory('Folder', 'folder2', title='Foo Folder 2')
        portal.folder1.folder2.invokeFactory('File', 'file1',
                                             title='Foo File 1')
        setRoles(portal, TEST_USER_ID, ['Member'])


class SearchPerformance100Layer(SearchLayer):

    def setUpPloneSite(self, portal):
        print "Testing performance with 100 pages"

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'test-folder')
        f = portal['test-folder']
        for i in range(0, 100):
            f.invokeFactory('Document', 'my-page'+str(i),
                            text='spam spam ham eggs')
        setRoles(portal, TEST_USER_ID, ['Member'])

        # Commit so that the test browser sees these objects
        import transaction
        transaction.commit()

    def tearDownPloneSite(self, portal):
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.manage_delObjects('test-folder')
        setRoles(portal, TEST_USER_ID, ['Member'])


class SearchPerformance1000Layer(SearchLayer):

    def setUpPloneSite(self, portal):
        print "Testing performance with 1000 pages"

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'test-folder')
        f = portal['test-folder']
        for i in range(0, 1000):
            f.invokeFactory('Document', 'my-page'+str(i),
                            text='spam spam ham eggs')
        setRoles(portal, TEST_USER_ID, ['Member'])

        # Commit so that the test browser sees these objects
        import transaction
        transaction.commit()

    def tearDownPloneSite(self, portal):
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.manage_delObjects('test-folder')
        setRoles(portal, TEST_USER_ID, ['Member'])


SEARCH_FIXTURE = SearchLayer()
SEARCH_SELENIUM_FIXTURE = SearchSeleniumLayer()
SEARCH_PERFORMANCE100_FIXTURE = SearchPerformance100Layer()
SEARCH_PERFORMANCE1000_FIXTURE = SearchPerformance1000Layer()

SEARCH_INTEGRATION_TESTING = IntegrationTesting(bases=(SEARCH_FIXTURE, ),
                                                name="Search:Integration")

SEARCH_SELENIUM_TESTING = \
    FunctionalTesting(bases=(SEARCH_SELENIUM_FIXTURE,
                             SELENIUM_PLONE_FUNCTIONAL_TESTING),
                             name="Search:Selenium")

SEARCH_PERFORMANCE100_FUNCTIONAL_TESTING = \
    FunctionalTesting(bases=(SEARCH_PERFORMANCE100_FIXTURE, ),
                             name="Search Performance 100:Functional")
SEARCH_PERFORMANCE1000_FUNCTIONAL_TESTING = \
    FunctionalTesting(bases=(SEARCH_PERFORMANCE1000_FIXTURE, ),
                             name="Search Performance 1000:Functional")


class SearchTestCase(unittest.TestCase):
    """We use this base class for all tahe tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit
    test cases.
    """
    layer = SEARCH_INTEGRATION_TESTING


class SearchSeleniumTestCase(SearchTestCase):
    """We use this base class for all tahe tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit
    test cases.
    """
    layer = SEARCH_SELENIUM_TESTING


class Search100FunctionalTestCase(SearchTestCase):
    """Test layer for performance testing with 100 objects
    """
    layer = SEARCH_PERFORMANCE100_FUNCTIONAL_TESTING


class Search1000FunctionalTestCase(SearchTestCase):
    """Test layer for performance testing with 1000 objects
    """
    layer = SEARCH_PERFORMANCE1000_FUNCTIONAL_TESTING
