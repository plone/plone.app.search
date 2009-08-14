from Products.Five.browser import BrowserView
from plone.app.contentlisting.interfaces import IContentListing
from Products.CMFCore.utils import getToolByName
from config import CRITERION
import json
from queryparser import QueryParser

class Search(BrowserView):
    
    def results(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog()
        if results:
            return IContentListing(results)
        return []

class AdvancedSearch(BrowserView):
    
    def __init__(self, context, request):
        self.results = None
        self.context = context
        self.request = request
        
        
    def getNumberOfResults(self):
        return len(self.results())

    def results(self):
        if self.results is None:
            results = self._queryForResults()
        return results
    
    def _queryForResults(self):
        # parse query
        query = QueryParser.parseFormquery(self.request.get('query',None))

        self.query = query
    
        # Get me my stuff!
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(query)
        if results:
            return IContentListing(results)
        return IContentListing([])
        
        
    def printQuery(self):
        return self.query
        
    def getConfig(self):
        return {'indexes':CRITERION}  
        # we wrap this in a dictionary so we can add more configuration data 
        # to the payload in the future. This is data that will be fetched 
        # by a browser AJAX call
         
        
    def getIndexesVocabulary(self):
        return CRITERION
        
    def getJavascriptConfig(self):
        template = """
        if (!window.plone_app_search) var window.plone_app_search = {}
        if (!window.plone_app_search.config) var window.plone_app_search.config = {}
        var window.plone_app_search.config = %s
        """
        return template%(json.dumps(self.getConfig()))
        
        