from Products.Five.browser import BrowserView
from plone.app.contentlisting.interfaces import IContentListing
from Products.CMFCore.utils import getToolByName


class Search(BrowserView):
    
    def results(self):
        
        formquery = self.request.get('query',None)
        if not formquery: 
            return []
        query = {}
        
        
        
        for row in formquery:
            v = row.get('v')
            if v:
                query.update({row.get('i') : v})
        self.query = query
        
        
        catalog = getToolByName(self.context, 'portal_catalog')
        return IContentListing(catalog(query))