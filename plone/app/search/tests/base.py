from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from collective.testcaselayer import ptc as tcl_ptc
from collective.testcaselayer import common

class Layer(tcl_ptc.BasePTCLayer):
    """Install plone.app.search"""

    def afterSetUp(self):
        ztc.installPackage('plone.app.layout')
        ztc.installPackage('plone.app.contentlisting')
        ztc.installPackage('plone.app.search')

        import plone.app.layout
        import plone.app.contentlisting
        import plone.app.search

        self.loadZCML('configure.zcml', package=plone.app.layout)
        self.loadZCML('configure.zcml', package=plone.app.contentlisting)
        self.loadZCML('configure.zcml', package=plone.app.search)

Installedlayer = Layer([common.common_layer])
UninstalledLayer = tcl_ptc.BasePTCLayer([common.common_layer])

class SearchTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit 
    test cases.
    """
    layer = Installedlayer

class SearchFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """
    layer = Installedlayer
