from Products.CMFCore.utils import getToolByName

class QueryParser(object):
    def parseFormquery(self, formquery):
        query = {}
        if not formquery:
            return query
            
        mt=getToolByName('portal_membership')
        user=mt.getAuthenticatedMember()
        current_username=''
        if user:
            current_username=user.getUserName()
            
        for row in formquery:
            index=row.get('i')
            values=row.get('v')
            criteria=row.get('c')

            if not values:
                continue
                
            # default behaviour
            tmp={index:values}
            
            # Ranges
            
            # query.i:records=modified&query.c:records=between&query.v:records:list=2009/08/12&query.v:records:list=2009/08/14
            # v[0] >= x > v[1]
            if criteria =='between':
                tmp={index:{
                    'query':values,
                    'range':'minmax'
                }}
            
            # query.i:records=modified&query.c:records=larger_then_or_equal&query.v:records=2009/08/12
            # x >= value
            elif criteria =='larger_then_or_equal':
                tmp={index:{
                    'query':values,
                    'range':'min'
                }}
            
            # query.i:records=modified&query.c:records=less_then&query.v:records=2009/08/14
            # x < value
            elif criteria =='less_then':
                tmp={index:{
                    'query':values,
                    'range':'max'
                }}
                
            # current user
            elif criteria=='current_user':
                tmp={'creator':current_username}
            
            elif criteria=='':
                tmp={index:value}
            
            query.update(tmp)
        return query