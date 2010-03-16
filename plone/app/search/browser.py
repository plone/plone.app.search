from urlparse import urlsplit
from os.path import basename
from Products.Five.browser import BrowserView
from plone.app.contentlisting.interfaces import IContentListing
from Products.CMFCore.utils import getToolByName
from config import CRITERION, SORTABLES
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

    @staticmethod
    def truncate_url(url, url_threshold=80, filename_threshold=20):
        """ Returns a cropped url.

        The goal is to display only the critical parts of the URL while keeping 
        the URL short enough to not stand out on the search results page.
        
        The url is first split into two parts: path and filename.
        
        Path truncating happens first. If the lenght of the whole url exceeds
        the url_threshold, then everything after the first '/' is truncated.
        
        After that we do the filename truncating (only if path truncating already happened).
        If the lenght of the filename exceeds the filename_threshold, 
        then everything after the {filename_thresholds}-th character is truncated.
        """
        
        # if url is short enough, just return it without any changes
        if len(url) < url_threshold:
            return url
        
        surl = urlsplit(url)    
        filename = basename(url)
        
        if len(filename) > filename_threshold:
            filename = filename[:filename_threshold] + '&hellip;'
        
        return "%s://%s/&hellip;/%s" %(surl.scheme, surl.netloc, filename)
