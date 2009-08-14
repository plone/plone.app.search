from Products.Five.browser import BrowserView
from plone.app.contentlisting.interfaces import IContentListing
from Products.CMFCore.utils import getToolByName
from config import CRITERION
import json
from queryparser import QueryParser
from zope.component import queryMultiAdapter
from ZTUtils import make_query

class Search(BrowserView):
    
    def results(self):
        return queryMultiAdapter((self.context, self.request),name='searchResults')()

    def getSortOptions(self):

        q = {}
        q.update(self.request.form)
        
        class sortoption(object):
            def __init__(self, request, title, sortkey=None, reverse=False):
                self.request = request
                self.title = title
                self.sortkey = sortkey
                self.reverse = reverse

            def selected(self):
                return self.request.get('sort_on') == self.sortkey
                
            def url(self):
                q = {}
                if self.request.get('SearchableText'):
                    q = {'SearchableText':self.request.get('SearchableText')}
                if self.sortkey:
                    q['sort_on'] = self.sortkey
                if self.reverse:
                    q['sort_order'] = 'reverse'
                return self.request.URL + '?' + make_query(q)

        return(
            sortoption(self.request, 'Relevance'),
            sortoption(self.request, 'Date (newest first)', 'Date', reverse=True),
            sortoption(self.request, 'Aphabetically', 'sortable_title'),
        )


class AdvancedSearch(BrowserView):
    
    def __init__(self, context, request):
        self._results = None
        self.context = context
        self.request = request
        
        
    def getNumberOfResults(self):
        return len(self._results())

    def results(self):
        if self._results is None:
            self._results = self._queryForResults()
        return self._results
    
    def _queryForResults(self):
        # parse query
        queryparser=QueryParser()
        query = queryparser.parseFormquery(self.request.get('query',None))

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
        var plone_app_search_config = %s
        """
        return template%(json.dumps(self.getConfig()))
        
        