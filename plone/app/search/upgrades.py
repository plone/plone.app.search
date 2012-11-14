from Products.CMFCore.utils import getToolByName
PROFILE = 'profile-plone.app.search:default'


def common(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(PROFILE)
