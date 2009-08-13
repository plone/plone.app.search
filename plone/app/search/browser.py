from Products.Five.browser import BrowserView
from plone.app.contentlisting.interfaces import IContentListing
from Products.CMFCore.utils import getToolByName


class Search(BrowserView):
    
    def results():
        catalog = getToolByName(self.context, 'portal_catalog')
        return IContentListing(catalog(query))