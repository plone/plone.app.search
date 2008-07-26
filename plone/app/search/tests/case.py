from Products.Five import zcml
from Testing import ZopeTestCase

# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase import PloneTestCase as ptc

# Set up a Plone site, and apply our custom extension profile
PROFILES = ('plone.app.search:default',)
ptc.setupPloneSite(extension_profiles=PROFILES)

import plone.app.search

class SearchLayer(PloneSite):
    @classmethod
    def setUp(cls):
        zcml.load_config('configure.zcml', plone.app.search)
        ZopeTestCase.installPackage("plone.browserlayer")

    @classmethod
    def tearDown(cls):
        pass


class IntegrationTestCase(ptc.PloneTestCase):
    """Base class for integration tests for the 'plone.app.search' product.

    This tests case sets up several things:

    - 'recipes' and 'tours' folders in the portal root which are marked as categories
    - both folders have a document in them with the word 'site' in its title
    - logs in as portal owner so we can tweak content
    """

    layer = SearchLayer

    def afterSetUp(self):
        super(IntegrationTestCase, self).afterSetUp()
        self.loginAsPortalOwner()
        ct=self.portal.portal_catalog

        self.portal.invokeFactory("Folder", "recipes", title="Recipes")
        self.setCategory(self.portal.recipes)
        self.portal.recipes.invokeFactory("Document", "pizza",
                title="The best recipe site on this site!")

        self.portal.invokeFactory("Folder", "tours", title="Tours")
        self.setCategory(self.portal.tours)
        self.portal.tours.invokeFactory("Document", "leiden",
                                        title="The best site in the country: Leiden")

        # We can't set description through invokeFactory
        self.portal.tours.leiden.setDescription("one two "*30)
        self.portal.portal_catalog.indexObject(self.portal.tours.leiden)


    def setCategory(self, obj, enabled=True):
        obj.Schema()["category"].set(obj, enabled)
        self.portal.portal_catalog.indexObject(obj)


    def createMemberarea(self, name):
        # bypass PTC's creation of a home folder for the default user
        pass

