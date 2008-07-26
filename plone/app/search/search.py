from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.app.schema.vocabulary import IVocabularyFactory
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.search.utils import quoteSearchString
from plone.memoize.view import memoize
from ZTUtils import make_query

class CategorySearchView(BrowserView):
    """View for a basic search.

    There are two basic search views:

    - search overview, which shows the top 5 five search results for each
      category
    - category search overview, which shows all search results for a
      specific category.

    The presence of a ``category`` request variable determines which view will
    be used.
    """

    template = ViewPageTemplateFile("search.pt")

    @property
    @memoize
    def _viewTypes(self):
        pp=getToolByName(self.context, "portal_properties")
        return pp.site_properties.typesUseViewActionInListings


    @property
    @memoize
    def _friendlyTypes(self):
        pu=getToolByName(self.context, "plone_utils")
        return pu.getUserFriendlyTypes()

    @property
    @memoize
    def _catalog(self):
        return getToolByName(self.context, "portal_catalog")


    def _brainInfo(self, brain):
        info=dict(url=brain.getURL(),
                  author=brain.Creator,
                  title=brain.Title,
                  description=self.crop(brain.Description),
                  review_state=self.normalize(brain.review_state),
                  portal_type=self.normalize(brain.portal_type),
                  relevance=brain.data_record_normalized_score_,
                  icon_url=self.icons_visible and self.site_url+brain.getIcon or None)
        if brain.portal_type in self._viewTypes:
            info["url"]+="/view"
        return info


    def _getCategoryBrain(self, category_id):
        def correct(c):
            return c.getPath()==category_id
        return filter(correct, self.categories())[0]


    def categorySearch(self, query, category, limit=None):
        info=self._brainInfo(category)
        info["search_url"]="%s?%s" % (self.request.URL,
                                      make_query(category=category.getPath(),
                                                 query=query))
        query=dict(path=category.getPath(),
                   portal_type=self._friendlyTypes,
                   SearchableText=quoteSearchString(query))
        results=self._catalog.search(query, limit=limit)
        if limit is not None:
            results=results[:limit]
        info["results"]=[self._brainInfo(brain) for brain in results]
        return info


    @memoize
    def categories(self):
        vocab=getUtility(IVocabularyFactory, name="plone.app.search.Categories")
        return self._catalog(
                object_provides="plone.app.search.interfaces.ICategory",
                order_by="sortable_title")


    def __init__(self, context, request):
        super(CategorySearchView, self).__init__(context, request)

        sp=getToolByName(context, "portal_properties").site_properties
        plone_view=getMultiAdapter((context, request), name="plone")
        self.icons_visible=plone_view.icons_visible()
        self.normalize=getUtility(IIDNormalizer).normalize
        self.site_url=getMultiAdapter((context, request),
                                    name="plone_portal_state").portal_url()+"/"
        def crop(text):
            return plone_view.cropText(text,
                    sp.search_results_description_length, sp.ellipsis)

        self.crop=crop


    def update(self):
        self.query=self.request.get("query", "")
        self.category_id=self.request.get("category", None)
        if self.category_id:
            category=self._getCategoryBrain(self.category_id)
            self.results=[self.categorySearch(self.query, category)]
        else:
            results=[self.categorySearch(self.query, category, 5)
                            for category in self.categories()]
            self.results=filter(lambda x: x['results'], results)


    def __call__(self):
        self.update()
        return self.template()
        

