from Products.CMFCore.utils import getToolByName
import DateTime

class QueryParser(object):
    def parseFormquery(self, formquery):
        query = {}
        if not formquery:
            return query
        mapping={
            'between': '_between',
            'larger_then_or_equal': '_largerThenOrEqual',
            'less_then': '_lessThen',
            'current_user': '_currentUser',
            'less_then_relative_date': '_lessThenRelativeDate',
            'more_then_relative_date': '_moreThenRelativeDate'
        }
        
        for row in formquery:
            index=row.get('i', None)
            operator=row.get('o', None)
            values=row.get('v', None)
            row.index=index
            row.operator=operator
            row.values=values

            if not values:
                continue
            
            # default behaviour
            tmp={index:values}
            
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
        tmp={'creator':self._getCurrentUsername()}
        return tmp

    # XXX check and fix
    # query.i:records=modified&query.o:records=less_then_relative_date&query.v:records=-7
    def _lessThenRelativeDate(self, row):
        values=row.values
        now=DateTime.now()
        my_date=now + values
        row.values=[now, my_date]
        raise ValueError(row.values)
        return self._between(row)
    
    # XXX check and fix
    def _moreThenRelativeDate(self, row):
        values=row.values
        now=DateTime.now()
        my_date=now = values
        return self._largerThenOrEqual(row)


    # Helper methods
    def _getCurrentUsername(self):
        mt=getToolByName('portal_membership')
        user=mt.getAuthenticatedMember()
        if user:
            return user.getUserName()
        return ''
        
    # XXX check and fix
    def _relativePathToAbsolutePath(self):
        # transform ../../.. to proper path for catalog querying
        pass
        
        
        
        
            
        