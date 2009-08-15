from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from copy import deepcopy

class QueryParser(object):
    def parseFormquery(self, formquery):
        query = {}
        if not formquery:
            return query
        formquery=deepcopy(formquery)
        mapping={
            'between': '_between',
            'larger_then_or_equal': '_largerThenOrEqual',
            'less_then': '_lessThen',
            'current_user': '_currentUser',
            'less_then_relative_date': '_lessThenRelativeDate',
            'more_then_relative_date': '_moreThenRelativeDate',
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

    # query.i:records=modified&query.o:records=less_then_relative_date&query.v:records=-7
    def _lessThenRelativeDate(self, row):
        values=int(row.values)

        now=DateTime()
        my_date=now + values
        
        my_date=my_date.earliestTime()
        row.values=my_date
        return self._lessThen(row)
        
        # place in right order
        if values>0:
            low,high=(now, my_date)
        else:
            low,high=(my_date, now)
    
    # query.i:records=modified&query.o:records=more_then_relative_date&query.v:records=-2
    def _moreThenRelativeDate(self, row):
        values=int(row.values)

        now=DateTime()
        my_date=now + values
        
        my_date=my_date.latestTime()
        row.values=my_date
        return self._largerThenOrEqual(row)
    
    # XXX check and fix
    def _relativePathToAbsolutePath(self):
        # transform ../../.. to proper path for catalog querying
        pass
        
    # Helper methods
    def _getCurrentUsername(self):
        mt=getToolByName('portal_membership')
        user=mt.getAuthenticatedMember()
        if user:
            return user.getUserName()
        return ''
        
        
        
        
            
        