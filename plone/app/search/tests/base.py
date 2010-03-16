from Testing import ZopeTestCase as ztc
from Testing.ZopeTestCase import Sandboxed

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from collective.testcaselayer.ptc import BasePTCLayer, ptc_layer

class Layer(BasePTCLayer):
    """Install plone.app.search"""

    def afterSetUp(self):
        fiveconfigure.debug_mode = True        
        from plone.app import layout, contentlisting, search

        zcml.load_config('configure.zcml', package=layout)
        zcml.load_config('configure.zcml', package=contentlisting)
        zcml.load_config('configure.zcml', package=search)
        
        fiveconfigure.debug_mode = False
        
        ptc.installPackage('plone.app.layout', quiet=True)
        ptc.installPackage('plone.app.contentlisting', quiet=True)
        ptc.installPackage('plone.app.search', quiet=True)

Installedlayer = Layer(bases=[ptc_layer])

ptc.setupPloneSite()

class SearchTestCase(Sandboxed, ptc.PloneTestCase):
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
