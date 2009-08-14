from Products.CMFCore.utils import getToolByName

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
        }
            
        for row in formquery:
            index=row.get('i')
            values=row.get('v')
            criteria=row.get('c')

            if not values:
                continue
            
            # default behaviour
            tmp={index:values}
            
            # exceptions
            if mapping.has_key(criteria):
                meth=getattr(self, mapping[criteria])
                tmp=meth( (index,criteria,values) )

            query.update(tmp)
            return query
            

    # Criteria
    
    # query.i:records=modified&query.c:records=between&query.v:records:list=2009/08/12&query.v:records:list=2009/08/14
    # v[0] >= x > v[1]
    def _between(self, row):
        index,criteria,values=row
        tmp={index:{
            'query':values,
            'range':'minmax'
        }}
        return tmp
            
    # query.i:records=modified&query.c:records=larger_then_or_equal&query.v:records=2009/08/12
    # x >= value
    def _largerTheOrEqual(self, row):
        index,criteria,values=row
        tmp={index:{
            'query':values,
            'range':'min'
        }}
        return tmp
    
    # query.i:records=modified&query.c:records=less_then&query.v:records=2009/08/14
    # x < value
    def _lessThen(self, row):
        index,criteria,values=row
        tmp={index:{
            'query':values,
            'range':'max'
        }}
        return tmp
        
    # current user
    def _currentUser(self, row):
        index,criteria,values=row
        tmp={'creator':self.getCurrentUsername()}
        return tmp
        
    def _lessThenRelativeDate(self, row):
        index,criteria,values=row
        now=DateTime.now()
        my_date=now + values
        tmp={index:{
            'query':[now, my_date],
            'range':'max'
        }}
        return tmp
        
    def _getCurrentUsername(self):
        mt=getToolByName('portal_membership')
        user=mt.getAuthenticatedMember()
        if user:
            return user.getUserName()
        return ''