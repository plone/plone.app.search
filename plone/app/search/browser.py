from Products.Five.browser import BrowserView
from plone.app.contentlisting.interfaces import IContentListing
from Products.CMFCore.utils import getToolByName


class Search(BrowserView):
    
    def results(self):
        # parse query
        query=self.parseFormquery(self.request.get('query',None))

        self.query = query
    
        # Get me my stuff!
        catalog = getToolByName(self.context, 'portal_catalog')
        results=catalog(query)
        if results:
            return IContentListing(catalog(query))
        return []
        
    def parseFormquery(self, formquery):
        query = {}
        for row in formquery:
            index=row.get('i')
            values=row.get('v')
            criteria=row.get('c')

            if not values:
                continue
                
            # default behaviour
            tmp={index:values}
            
            # ranges
            if criteria =='between':
                tmp={index:{
                    'query':values,
                    'range':'minmax'
                }}
            
            query.update(tmp)
        return query
        
        
        
# query.i:records=modified&query.c:records=between&query.v:records:list=2009/01/01&query.v:records:list=2009/10/01