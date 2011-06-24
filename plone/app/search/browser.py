from plone.app.contentlisting.interfaces import IContentListing
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from zope.i18nmessageid import MessageFactory
from zope.publisher.browser import BrowserView
from ZTUtils import make_query

_ = MessageFactory('plone')


class Search(BrowserView):

    def __init__(self, context, request):
        super(Search, self).__init__(context, request)
        self.sections_cache = {}

    def results(self, query, batch=False, b_size=30, b_start=0, orphan=1):
        """ Get properly wrapped search results from the catalog.
        Everything in Plone that performs searches should go through this view.
        'query' should be a dictionary of catalog parameters.
        """
        if not query:
            return IContentListing([])

        # In order to wrap the catalog results with some checkups like prevent
        # site error when searching for '*' we don't call catalog directly, but
        # queryCatalog instead. We also want to filter the results through the
        # script's ensureFriendlyTypes() in order to get rid of unwanted content
        # types (like different Criteria types) in the output, hence:
        # show_all=1, use_types_blacklist=True parameters in the call.
        # 
        # We also want to get items starting from the navigation root, that is
        # not necessary the site's root. This lets us build language folders
        # structures like en/ no/ and make sure the search results we are
        # getting within no/ don't show the ones coming from en/.
        # use_navigation_root=True takes care of this.
        if batch:
            b_start = int(b_start)
            query['b_start'] = b_start
            query['b_size'] = b_size + orphan
            results = IContentListing(self.context.queryCatalog(query,
                show_all=1, use_types_blacklist=True, use_navigation_root=True))
            batch = Batch(results, b_size, b_start, orphan=orphan)
            return IContentListing(batch)

        return IContentListing(self.context.queryCatalog(query, show_all=1,
            use_types_blacklist=True, use_navigation_root=True))

    def sort_options(self):
        """ Sorting options for search results view. """
        return (
            SortOption(self.request, _(u'relevance'), ''),
            SortOption(self.request, _(u'date (newest first)'),
                'Date', reverse=True),
            SortOption(self.request, _(u'alphabetically'), 'sortable_title'),
        )

    def show_advanced_search(self):
        """Whether we need to show advanced search options a.k.a. filters?"""
        show = self.request.get('advanced_search', None)
        if not show or show == 'False':
            return False
        return True

    def advanced_search_trigger(self):
        """URL builder for show/close advanced search filters."""
        query = self.request.get('QUERY_STRING', None)
        url = self.request.get('ACTUAL_URL', self.context.absolute_url())
        if not query:
            return url
        if 'advanced_search' in query:
            if 'advanced_search=True' in query:
                query = query.replace('advanced_search=True', '')
            if 'advanced_search=False' in query:
                query = query.replace('advanced_search=False', '')
        else:
            query = query + '&advanced_search=True'
        return url + '?' + query

    def section(self, url):
        """ Returns a section in which the object at the passed url is
        contained. Section is a first-level folder in Plone root.

        For objects that are contained in Plone root object, we just return
        None as we don't want to display anything on the template.

        It does that by first removing the portal url part from the object's
        url, including the Plone instance id in non-virtual-hostname
        environments.

        Then it splits the path with '/', taking the second item which is
        the section's id.

        Lastly an object is retrieved from the Plone root object that has
        the id of the section we are looking for.

        Simple caching is put in place to prevent waking up section object for
        objects under the same section.

        TODO: Review how this interacts with navigation root and virtual
        hosting (hannosch)
        """
        # plone root object
        url_tool = getToolByName(self.context, "portal_url")
        portal = url_tool.getPortalObject()

        # truncate away http, domain and plone instance id
        path = url.split(url_tool.getPortalPath())[1]

        # don't show location for first-level objects
        # -> ['', 'front-page']
        if len(path.split('/')) < 3:
            return None

        # get sections's id
        section_id = path.split('/')[1]

        # is this section's Title already stored in sections_cache cache
        # dictionary?
        section = self.sections_cache.get(section_id, None)
        if section is not None:
            return section

        # get section object
        section = portal[section_id]

        # store title and id in cache
        self.sections_cache[section_id] = title = section.Title()
        return title


class SortOption(object):

    def __init__(self, request, title, sortkey='', reverse=False):
        self.request = request
        self.title = title
        self.sortkey = sortkey
        self.reverse = reverse

    def selected(self):
        sort_on = self.request.get('sort_on', '')
        return sort_on == self.sortkey

    def url(self):
        q = {}
        q.update(self.request.form)
        if 'sort_on' in q.keys():
            del q['sort_on']
        if 'sort_order' in q.keys():
            del q['sort_order']
        q['sort_on'] = self.sortkey
        if self.reverse:
            q['sort_order'] = 'reverse'

        base_url = self.request.URL
        # After the AJAX call the request is changed and thus the URL part of
        # it as well. In this case we need to tweak the URL to point to have
        # correct URLs
        if '@@updated_search' in base_url:
            base_url = base_url.replace('@@updated_search', '@@search')
        return base_url + '?' + make_query(q)
