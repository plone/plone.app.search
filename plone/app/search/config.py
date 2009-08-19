# (temporary) Static config for plone.app.search
# ===================================================
# This has to be in the plone.app.registry later on. (preferable)

# CRITERION contains the searchable indexes and their operators and widgettypes
# SORTABLES contains the sortable indexes

# note: a view types a commented, because there is something about them
# see description/header per item



CRITERION={
    'Subject':{
        'friendly_name': 'Categories',
        'description': 'The category the item is put in.',
        'operators':{
            'is_not':{
                'friendly_name' : 'are not',
                'widget'        : 'MultipleSelectionWidget',
            },
            'is':{
                'friendly_name' : 'are',
                'widget'        : 'MultipleSelectionWidget',
            },
        },
        'values': {
            'Plone':{
                'friendly_name' : 'Plone',
            },
            'Zope':{
                'friendly_name' : 'Zope',
            },
            'Python':{
                'friendly_name' : 'Python',
            },
            'Javascript':{
                'friendly_name' : 'Javascript',
            },
        },
    },

    'Creator':{
        'friendly_name': 'Creator',
        'description': 'The creator of the item',
        'operators':{
            'is_not':{
                'friendly_name' : 'does not equal',
                'widget'        : 'StringWidget',
                'description'   : 'Only username search is supported.',
            },
            'is':{
                'friendly_name' : 'equals',
                'widget'        : 'StringWidget',
                'description'   : 'Only username search is supported',
            },
        },
    },

    'created':{
        'friendly_name': 'Creation date',
        'description': 'The time and date an item was created',
        'operators':{
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
    },

    'Description':{
        'friendly_name': 'Description',
        'description': 'Description',
        'operators':{
            'is_not':{
                'friendly_name' : 'does not equal',
                'widget'        : 'StringWidget',
                'description'   : 'Tip: you can use * to autocomplete.',
            },
            'is':{
                'friendly_name' : 'equals',
                'widget'        : 'StringWidget',
                'description'   : 'Tip: you can use * to autocomplete.',
            },
        },
    },

    'effective':{
        'friendly_name': 'Effective date (publish date)',
        'description': 'The time and date an item becomes publicly available',
        'operators':{
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
    },

    'end':{
        'friendly_name': 'End date (event)',
        'description': 'The end date and time of an event',
        'operators':{
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
    },

    'expires':{
        'friendly_name': 'Expiration date',
        'description': 'The time and date an item is no longer publicly available',
        'operators':{
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
    },

    'Type':{
        'friendly_name': 'Item type',
        'description': 'An item\'s type (e.g. Event)',
        'operators':{
            'is_not':{
                'friendly_name' : 'does not equal',
                'widget'        : 'MultipleSelectionWidget',
            },
            'is':{
                'friendly_name' : 'equals',
                'widget'        : 'MultipleSelectionWidget',
            },
        },
        'values': {
            'Page':{
                'friendly_name' : 'Page',
# possible extension/option
#               'preselected' : True,
            },
            'Folder':{
                'friendly_name' : 'Folder',
            },
            'File':{
                'friendly_name' : 'File',
            },
            'Collection':{
                'friendly_name' : 'Collection',
            },
        },
    },

    'path':{
        'friendly_name': 'Location (path)',
        'description': 'The location of an item in the site (path)',
        'operators':{
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
    },

    'modified':{
        'friendly_name': 'Modification date',
        'description': 'The time and date an item was last modified',
        'operators':{
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
    },

    'getRawRelatedItems':{
        'friendly_name': 'Related to',
        'description': 'Find items related to the selected items',
        'operators':{
            'to':{
                'friendly_name' : 'to',
                'widget'        : 'MultipleSelectionWidget',
            },
        },
    },

    'SearchableText':{
        'friendly_name': 'Search text',
        'description': 'Text search of an item\'s contents',
        'operators':{
            'is_not':{
                'friendly_name' : 'does not equal',
                'widget'        : 'StringWidget',
                'description'   : 'Tip: you can use * to autocomplete.',
            },
            'is':{
                'friendly_name' : 'equals',
                'widget'        : 'StringWidget',
                'description'   : 'Tip: you can use * to autocomplete.',
            },
        },
    },

    'getId':{
        'friendly_name': 'Short name',
        'description': 'Short name of the item',
        'operators':{
            'is_not':{
                'friendly_name' : 'does not equal',
                'widget'        : 'StringWidget',
            },
            'is':{
                'friendly_name' : 'equals',
                'widget'        : 'StringWidget',
            },
        },
    },

    'start':{
        'friendly_name': 'Start date',
        'description': 'The start date and time of an event',
        'operators':{
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
    },

    'review_state':{
        'friendly_name': 'State',
        'description': 'An item\'s workflow state (e.g.published)',
        'operators':{
            'is_not':{
                'friendly_name' : 'does not equal',
                'widget'        : 'MultipleSelectionWidget',
            },
            'is':{
                'friendly_name' : 'equals',
                'widget'        : 'MultipleSelectionWidget',
            },
        },
        'values': {
            'Published':{
                'friendly_name' : 'Published',
            },
            'Private':{
                'friendly_name' : 'Private',
            },
            'Pending':{
                'friendly_name' : 'Pending',
            },
            'Rejected':{
                'friendly_name' : 'Rejected',
            },
            'Sent_back':{
                'friendly_name' : 'Sent Back',
            },
            'Draft':{
                'friendly_name' : 'Draft',
            },
        },
    },

    'Title':{
        'friendly_name': 'Title',
        'description': 'Title of the item',
        'operators':{
            'is_not':{
                'friendly_name' : 'does not equal',
                'widget'        : 'StringWidget',
                'description'   : 'Tip: you can use * to autocomplete.',
            },
            'is':{
                'friendly_name' : 'equals',
                'widget'        : 'StringWidget',
                'description'   : 'Tip: you can use * to autocomplete.',
            },
        },
    },
}


SORTABLES={
    'Creator':{
        'friendly_name' : 'Creator',
        'description' : 'The creator (username) of the item',
    },
    'Type':{
        'friendly_name' : 'Item Type',
        'description' : 'The type of the item',
    },
# is there an usecase?
#     'getId':{  
#          'friendly_name' : 'Short name',
#          'description' : 'The short name of the item',
#     },
# same as getId?
#     'id':{  
#          'friendly_name' : 'ID',
#          'description' : '',
#     },
# this is portal type, such as document (not page), topic (not collection)
#     'portal_type':{  
#          'friendly_name' : '',
#          'description' : '',
#     },
    'review_state':{  
        'friendly_name' : 'State',
        'description' : 'An item\'s workflow state (e.g.published)',
    },
    'sortable_title':{  
        'friendly_name' : 'Title',
        'description' : 'An item\'s title transformed for sorting',
    },
# Same as Modification Date?
#     'Date':{  
#          'friendly_name' : 'Date',
#          'description' : '',
#     },
    'created':{  
        'friendly_name' : 'Creation date',
        'description' : 'The time and date an item was created',
    },
    'effective':{  
        'friendly_name' : 'Effective date',
        'description' : 'The time and date an item becomes publicly available',
    },
    'end':{  
        'friendly_name' : 'End date (Event)',
        'description' : 'The end date and time of an event',
    },
    'expires':{  
        'friendly_name' : 'Expire date',
        'description' : 'The time and date an item is no longer publicly available',
    },
    'modified':{  
        'friendly_name' : 'Modification date',
        'description' : 'The time and date an item was last modified',
    },
    'start':{  
        'friendly_name' : 'Start date',
        'description' : 'The start date and time of an event',
    },
    'Subject':{  
        'friendly_name' : 'Categories',
        'description' : 'The keywords used to describe an item',
    },
    'getEventType':{  
        'friendly_name' : 'Event type',
        'description' : 'The type of event',
    },
# use case?
#     'getRawRelatedItems':{  
#          'friendly_name': 'Related to',
#          'description': 'Find items related to the selected items',
#     },
    'relevence':{
        'friendly_name' : 'Relevence',
        'description' : 'Relevence',
    },
}
