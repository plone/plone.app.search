# temporary dynamic config for plone.app.search
# ===================================================
# This has to be in the plone.app.registry later on. (preferable)

# SearchConfig.criterion contains the searchable indexes and their operators and widgettypes
# SearchConfig.sortables contains the sortable indexes

# note: a view types a commented, because there is something about them
# see description/header per item

try: # python >= 2.7
    from collections import OrderedDict
except: # python >= 2.4 < 2.7
    from collective.ordereddict import OrderedDict
    
from Products.CMFCore.utils import getToolByName
import operator

# Temporary dynamic solution, need to use
# Fetches everything from portal_catalog

class SearchConfig(object):
    def __init__(self, context, request):
        self.context=context
        self.request=request
        
        self.ignorable_indexes=['', '']
        self.indextypes_values=['FieldIndex', 'KeywordIndex']
        
        self.pctool = getToolByName( self.context, 'portal_catalog')

    @property
    def criterion(self):
        indexes=self.getIndexes()
        result=OrderedDict()
        for index in indexes:
            operators=self.getOperatorsForIndex(index)
            values=self.getValuesForIndex(index)
            tmp=OrderedDict()
            tmp['friendly_name'] = index.title or index.getId() # Temporary "solution"
            tmp['description'] = index.title or index.getId() # Temporary "solution"
            tmp['operators'] = operators

            if values:
                tmp['values']=values
            result[index.getId()]=tmp

        return result
        
    def getIndexes(self):
        """ Return a list of indexes from portal_catalog. """
        pcatalog = getToolByName( self.context, 'portal_catalog')
        indexes=pcatalog.getIndexObjects()
        val=[(str(index.title or index.getId()).lower(), index) for index in indexes]
        val.sort(key=operator.itemgetter(0))
        indexes=[x[1] for x in val]
        return indexes
        
    def getOperatorsForIndex(self, index):
        return self.getOperatorsForIndexType(index.meta_type)
        
    def getOperatorsForIndexType(self, type):
        operators=self.getOperators()
        if operators.has_key(type):
            return operators[type]
        return {}
        
    def getOperators(self):
        tmp={
            'ZCTextIndex': {
                'is':{
                    'friendly_name' : 'equals',
                    'widget'        : 'StringWidget',
                    'description'   : 'Tip: you can use * to autocomplete.',
                },
                'is_not':{
                    'friendly_name' : 'does not equal',
                    'widget'        : 'StringWidget',
                    'description'   : 'Tip: you can use * to autocomplete.',
                },
            },
            'FieldIndex': {
                'is':{
                    'friendly_name' : 'equals',
                    'widget'        : 'MultipleSelectionWidget',
                },
                'is_not':{
                    'friendly_name' : 'does not equal',
                    'widget'        : 'MultipleSelectionWidget',
                },
            },
            'KeywordIndex': {
                'is':{
                    'friendly_name' : 'are',
                    'widget'        : 'MultipleSelectionWidget',
                },
                'is_not':{
                    'friendly_name' : 'are not',
                    'widget'        : 'MultipleSelectionWidget',
                },
            },
            'PathIndex': {
                'is':{
                    'friendly_name' : 'location in the site',
                    'widget'        : 'ReferenceWidget',
                    'description'   : 'Fill in your absolute location e.g.: /site/events/',
                },
                'relative_location':{
                    'friendly_name' : 'location in site relative to the current location',
                    'widget'        : 'RelativePathWidget',
                    'description'   : 'Enter a relative path e.g.:\'..\' for the parent folder \'../..\' for the parent\'s parent \'../somefolder\' for a sibling folder',
                },
            },
            'ExtendedPathIndex': {
                'is':{
                    'friendly_name' : 'location in the site',
                    'widget'        : 'ReferenceWidget',
                    'description'   : 'Fill in your absolute location e.g.: /site/events/',
                },
                'relative_location':{
                    'friendly_name' : 'location in site relative to the current location',
                    'widget'        : 'RelativePathWidget',
                    'description'   : 'Enter a relative path e.g.:\'..\' for the parent folder \'../..\' for the parent\'s parent \'../somefolder\' for a sibling folder',
                },
            },
            'DateIndex': {
                'less_then':{
                    'friendly_name': 'before',
                    'widget': 'DateWidget',
                    'description'   : 'please use YYYY/MM/DD.',
                },
                'is':{
                    'friendly_name': 'on',
                    'widget': 'DateWidget',
                    'description'   : 'please use YYYY/MM/DD.',
                },
                'larger_then':{
                    'friendly_name': 'after',
                    'widget': 'DateWidget',
                    'description'   : 'please use YYYY/MM/DD.',
                },
                'between':{
                    'friendly_name': 'between',
                    'widget': 'DateRangeWidget',
                    'description'   : 'please use YYYY/MM/DD.',
                },
            },
        }
        return tmp
    
    def getValuesForIndex(self, index):
        id=index.getId()
        if id in self.indextypes_values:
            return self.pctool.uniqueValuesFor(index.getId())
        return None
    
    @property
    def sortables(self):
        return {}
