from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from copy import deepcopy
from Acquisition import aq_parent

class QueryParser(object):
    
    def __init__(self, context, request):
        self.context=context
        self.request=request
    
    def parseFormquery(self, formquery=None):
        formquery=formquery or getattr(self.request, 'query', None)
        if not formquery:
            return {}

        formquery=deepcopy(formquery)
        mapping={
            'between': '_between',
            'larger_then_or_equal': '_largerThenOrEqual',
            'less_then': '_lessThen',
            'current_user': '_currentUser',
            'less_then_relative_date': '_lessThenRelativeDate',
            'more_then_relative_date': '_moreThenRelativeDate',
            'path': '_path',
            'relative_path': '_relativePath',
        }
        
        query = {}
        for row in formquery:
            index=row.get('i', None)
            operator=row.get('o', None)
            values=row.get('v', None)
            row.index=index
            row.operator=operator
            row.values=values
            
            # default behaviour
            tmp={index:{
                'query':values
            }}
            
            if mapping.has_key(operator):
                meth=getattr(self, mapping[operator])
                tmp=meth( row )

            query.update(tmp)
        return query

    # operators
    
    # query.i:records=modified&query.o:records=between&query.v:records:list=2009/08/12&query.v:records:list=2009/08/14
    # v[0] >= x > v[1]
    def _between(self, row):
        tmp={row.index:{
            'query':row.values,
            'range':'minmax'
        }}
        return tmp
            
    # query.i:records=modified&query.o:records=larger_then_or_equal&query.v:records=2009/08/12
    # x >= value
    def _largerThenOrEqual(self, row):
        tmp={row.index:{
            'query':row.values,
            'range':'min'
        }}
        return tmp
    
    # query.i:records=modified&query.o:records=less_then&query.v:records=2009/08/14
    # x < value
    def _lessThen(self, row):
        tmp={row.index:{
            'query':row.values,
            'range':'max'
        }}
        return tmp
        
    # current user
    def _currentUser(self, row):
        tmp={row.index:{
            'query': self.getCurrentUsername()
        }}
        return tmp

    # query.i:records=modified&query.o:records=less_then_relative_date&query.v:records=-7
    def _lessThenRelativeDate(self, row):
        values=int(row.values)

        now=DateTime()
        my_date=now + values
        
        my_date=my_date.earliestTime()
        row.values=my_date
        return self._lessThen(row)
    
    # query.i:records=modified&query.o:records=more_then_relative_date&query.v:records=-2
    def _moreThenRelativeDate(self, row):
        values=int(row.values)

        now=DateTime()
        my_date=now + values
        
        my_date=my_date.latestTime()
        row.values=my_date
        return self._largerThenOrEqual(row)
    
    # query.i:records=path&query.o:records=path&query.v:records=/search/news/
    # query.i:records=path&query.o:records=path&query.v:records=08fb402c83d0e68cf4d547ea79f7680c
    def _path(self, row):
        values=row.values
        
        # UID
        if not '/' in values:
            row.values=self.getPathByUID(values)
        
        tmp={row.index:{
            'query':row.values
        }}
        
        depth = getattr(row, 'depth', None)
        if depth is not None: # can be 0
            tmp[row.index]['depth']=int(depth)
        return tmp
        
    # query.i:records=path&query.o:records=relative_path&query.v:records=../../..
    def _relativePath(self, row):
        t=len([x for x in row.values.split('/') if x])
        
        obj=self.context
        for x in xrange(t):
            obj=aq_parent(obj)

        if obj and hasattr(obj, 'getPhysicalPath'):
            row.values='/'.join(obj.getPhysicalPath())
            return self._path(row)
        
        row.values='/'.join(obj.getPhysicalPath())
        return self.path(row)
        
    # Helper methods
    def getCurrentUsername(self):
        mt=getToolByName('portal_membership')
        user=mt.getAuthenticatedMember()
        if user:
            return user.getUserName()
        return ''

    def getPathByUID(self):
        """Returns the path of an object specified in the request by UID"""

        context = self.context
        request = context.REQUEST

        if not hasattr(request, 'uid'):
        	return ""

        uid = request['uid']

        reference_tool = getToolByName(context, 'reference_catalog')
        obj = reference_tool.lookupObject(uid)

        if obj:
        	return obj.absolute_url()

        return ""