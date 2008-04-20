from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.search.utils import currentCategory

class SearchViewlet(ViewletBase):
    """A category-capable search viewlet."""

    def update(self):
        super(SearchViewlet, self).update()
        self.category_id=category=currentCategory(self.context)
        if self.category_id is not None:
            self.category_id="/".join(category.getPhysicalPath())

    render = ViewPageTemplateFile("viewlet.pt")

