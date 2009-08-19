from Products.Five.browser import BrowserView
from plone.app.contentlisting.interfaces import IContentListing
from Products.CMFCore.utils import getToolByName
from config import CRITERION, SORTABLES
import json
from queryparser import QueryParser
from zope.component import queryMultiAdapter, getMultiAdapter
from ZTUtils import make_query

class Search(BrowserView):

    def results(self, batch=False, b_size=30):
        query = {}
        query.update(getattr(self.request, 'form',{}))
            #query.update(dict(getattr(self.request, 'other',{})))
        if not query:
            return IContentListing([])
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(query)
        
        if batch:
            from Products.CMFPlone import Batch
            b_start = self.request.get('b_start', 0)
            batch = Batch(results, b_size, int(b_start), orphan=0)
            return IContentListing(batch)
        return IContentListing(results)


    def getSortOptions(self):
        """ options for sorting in the search result template, also for marking selected """
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
            sortoption(self.request, 'relevance'),
            sortoption(self.request, 'date (newest first)', 'Date', reverse=True),
            sortoption(self.request, 'aphabetically', 'sortable_title'),
        )


class AdvancedSearch(BrowserView):
    """ """
    
    # This is the advanced search that uses the query view from new-style-collections.
    # If we end up not using this view for advanced search, it should probably be moved to the collections 
    # package
    
    def __init__(self, context, request):
        self._results = None
        self.context = context
        self.request = request

    def getNumberOfResults(self):
        return len(self.results())

    def getFormattedNumberOfResults(self):
        return "%d items remaining" % (len(self.results()))

    def results(self):
        if self._results is None:
            self._results = self._queryForResults()
        return self._results
    
    def _queryForResults(self, formquery=None):
        # parse query
        if not formquery:
            formquery=self.request.get('query', None)
        queryparser=QueryParser(self.context, self.request)
        query = queryparser.parseFormquery(formquery)

        if not query:
            return IContentListing([])

        # sorting
        query['sort_on'] = getattr(self.request, 'sort_on', 'getObjPositionInParent')
        query['sort_order'] = getattr(self.request, 'sort_order', 'ascending')

        # Get me my stuff!
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(query)

        if results:
            return IContentListing(results)
        return IContentListing([])

    def printQuery(self):
        return self.query

    def getConfig(self):
        return {'indexes':CRITERION, 'sortable_indexes': SORTABLES}
        # we wrap this in a dictionary so we can add more configuration data 
        # to the payload in the future. This is data that will be fetched 
        # by a browser AJAX call

    def getJSONConfig(self):
        return json.dumps(self.getConfig())

    def previewSearchResults(self):
        return getMultiAdapter((self.context, self.request),name='previewadvancedsearchresults')()
