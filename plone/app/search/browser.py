from plone.app.contentlisting.interfaces import IContentListing
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import getNavigationRoot
from Products.CMFPlone.PloneBatch import Batch
from Products.ZCTextIndex.ParseTree import ParseError
from zope.i18nmessageid import MessageFactory
from zope.publisher.browser import BrowserView
from ZTUtils import make_query

_ = MessageFactory('plone')

# We should accept both a simple space, unicode u'\u0020 but also a
# multi-space, so called 'waji-kankaku', unicode u'\u3000'
MULTISPACE = u'\u3000'.encode('utf-8')


def quote_bad_chars(s):
    # We need to quote parentheses when searching text indices
    if '(' in s:
        s = s.replace('(', '"("')
    if ')' in s:
        s = s.replace(')', '")"')
    return s


class Search(BrowserView):

    def __init__(self, context, request):
        super(Search, self).__init__(context, request)
        self.sections_cache = {}

    def results(self, query=None, b_size=10, b_start=0, orphan=1):
        """ Get properly wrapped search results from the catalog.
        Everything in Plone that performs searches should go through this view.
        'query' should be a dictionary of catalog parameters.
        """
        if query is None:
            query = {}
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

        query['b_start'] = b_start = int(b_start)
        query['b_size'] = b_size + orphan
        results = IContentListing(self.query(query))
        return Batch(results, b_size, b_start, orphan=orphan)

    def query(self, query):
        context = self.context
        request = self.request

        show_query = True
        quote_logic_indexes = ['SearchableText', 'Description', 'Title']
        use_types_blacklist = True
        show_inactive = False
        use_navigation_root = True

        results = []
        catalog = getToolByName(context, 'portal_catalog')
        indexes = catalog.indexes()
        second_pass = {}

        def ensureFriendlyTypes(query):
            ploneUtils = getToolByName(context, 'plone_utils')
            portal_type = query.get('portal_type', [])
            if not isinstance(portal_type, list):
                portal_type = [portal_type]
            Type = query.get('Type', [])
            if not isinstance(Type, list):
                Type = [Type]
            typesList = portal_type + Type
            if not typesList:
                friendlyTypes = ploneUtils.getUserFriendlyTypes(typesList)
                query['portal_type'] = friendlyTypes

        def rootAtNavigationRoot(query):
            if 'path' not in query:
                query['path'] = getNavigationRoot(context)

        # Avoid creating a session implicitly.
        for k in request.keys():
            if k in ('SESSION',):
                continue
            v = request.get(k)
            if v and k in indexes:
                if k in quote_logic_indexes:
                    v = quote_bad_chars(v)
                    if MULTISPACE in v:
                        v = v.replace(MULTISPACE, ' ')
                query[k] = v
                show_query = 1
            elif k.endswith('_usage'):
                key = k[:-6]
                param, value = v.split(':')
                second_pass[key] = {param:value}
            elif k in ('sort_on', 'sort_order', 'sort_limit'):
                if k == 'sort_limit' and not isinstance(v, int):
                    query[k] = int(v)
                else:
                    query[k] = v

        for k, v in second_pass.items():
            qs = query.get(k)
            if qs is None:
                continue
            query[k] = q = {'query':qs}
            q.update(v)

        # doesn't normal call catalog unless some field has been queried
        # against. if you want to call the catalog _regardless_ of whether
        # any items were found, then you can pass show_all=1.
        if show_query:
            try:
                if use_types_blacklist:
                    ensureFriendlyTypes(query)
                if use_navigation_root:
                    rootAtNavigationRoot(query)
                query['show_inactive'] = show_inactive
                results = catalog(**query)
            except ParseError:
                pass

        return results

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
