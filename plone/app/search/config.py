# (temporary) Static config for plone.app.search
# ===================================================
# This has to be in the plone.app.registry later on. (preferable)

# CRITERION contains the searchable indexes and their operators and widgettypes
# SORTABLES contains the sortable indexes

# note: a view types a commented, because there is something about them
# see description/header per item



CRITERION={
         'Subject':{
                  'friendly_name': 'Subject',
                  'description': 'The subject',
                  'operators':{
                           'is_not':{
                                    'friendly_name' : 'Does not equal',
                                    'widget'        : 'StringWidget',
                                    },
                          'is':{
                                    'friendly_name' : 'Equals',
                                    'widget'        : 'StringWidget',},
                           },
                  },
         'Creator':{
                  'friendly_name': 'Creator',
                  'description': 'The creator of the item',
                  'operators':{
                           'is_not':{
                                    'friendly_name' : 'Does not equal',
                                    'widget'        : 'StringWidget',
                                    },
                          'is':{
                                    'friendly_name' : 'Equals',
                                    'widget'        : 'StringWidget',},
                           },
                  },
         'created':{
                  'friendly_name': 'Creation date',
                  'description': 'The time and date an item was created',
                  'operators':{
                           'smaller_or_equal':{
                                    'friendly_name': 'Before',
                                    'widget': 'DateWidget',
                                    },
                          'is':{
                                    'friendly_name': 'On',
                                    'widget': 'DateWidget',
                                    },
                          'larger_then':{
                                    'friendly_name': 'After',
                                    'widget': 'DateWidget',
                                    },
                           'between':{
                                    'friendly_name': 'Between',
                                    'widget': 'DateRangeWidget',
                                    },
                           },
                  }, 
         'Description':{
                  'friendly_name': 'Description',
                  'description': 'Description',
                  'operators':{
                           'is_not':{
                                    'friendly_name' : 'Does not equal',
                                    'widget'        : 'StringWidget',
                                    },
                            
                           'is':{
                                    'friendly_name' : 'Equals',
                                    'widget'        : 'StringWidget'
                                    ,},
                           },
                  },
         'effective':{
                  'friendly_name': 'Effective date (publish date)',
                  'description': 'The time and date an item becomes publicly available',
                  'operators':{
                           'smaller_or_equal':{
                                    'friendly_name': 'Before',
                                    'widget': 'DateWidget',
                                    },
                          'is':{
                                    'friendly_name': 'On',
                                    'widget': 'DateWidget',
                                    },
                          'larger_then':{
                                    'friendly_name': 'After',
                                    'widget': 'DateWidget',
                                    },
                           'between':{
                                    'friendly_name': 'Between',
                                    'widget': 'DateRangeWidget',
                                    },
                           },

                  },
         'end':{
                  'friendly_name': 'End date (event)',
                  'description': 'The end date and time of an event',
                  'operators':{
                           'smaller_or_equal':{
                                    'friendly_name': 'Before',
                                    'widget': 'DateWidget',
                                    },
                           'is':{
                                    'friendly_name': 'On',
                                    'widget': 'DateWidget',
                           },
                           'larger_then':{
                                    'friendly_name': 'After',
                                    'widget': 'DateWidget',
                                    },
                           'between':{
                                    'friendly_name': 'Between',
                                    'widget': 'DateRangeWidget',
                                    },
                           },

                    
                  },
         'expires':{
                  'friendly_name': 'Expiration date',
                  'description': 'The time and date an item is no longer publicly available',
                  'operators':{
                           'smaller_or_equal':{
                                    'friendly_name': 'Before',
                                    'widget': 'DateWidget',
                                    },
                          'is':{
                                    'friendly_name': 'On',
                                    'widget': 'DateWidget',
                                    },
                          'larger_then':{
                                    'friendly_name': 'After',
                                    'widget': 'DateWidget',
                                    },
                           'between':{
                                    'friendly_name': 'Between',
                                    'widget': 'DateRangeWidget',
                                    },
                           },
                  

                  },
         'Type':{
                  'friendly_name': 'Item type',
                  'description': 'An item\'s type (e.g. Event)',
                  'operators':{
                           'is_not':{
                                    'friendly_name' : 'Does not equal',
                                    'widget'        : 'MultipleSelectionWidget',
                                    },
                           'is':{
                                    'friendly_name' : 'Equals',
                                    'widget'        : 'MultipleSelectionWidget',
                                    },
                           },
                  'values': {
                           'Page':{
                                    'friendly_name' : 'Page',
# possible extension/option
#                                    'preselected' : True,
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
                                    'friendly_name' : 'Location in the site',
                                    'widget'        : 'ReferenceWidget',
                           },
                           'relative_location':{
                                    'friendly_name' : 'Location in site relative to the current location',
                                    'widget'        : 'RelativePathWidget',
                                    },
                           },
                  },
         'modified':{
                  'friendly_name': 'Modification date',
                  'description': 'The time and date an item was last modified',
                  'operators':{
                           'smaller_or_equal':{
                                    'friendly_name': 'Before',
                                    'widget': 'DateWidget',
                                    },
                           'is':{
                                    'friendly_name': 'On',
                                    'widget': 'DateWidget',
                           },
                           'larger_then':{
                                    'friendly_name': 'After',
                                    'widget': 'DateWidget',
                                    },
                           'between':{
                                    'friendly_name': 'Between',
                                    'widget': 'DateRangeWidget',
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
                                    'friendly_name' : 'Does not equal',
                                    'widget'        : 'StringWidget',
                                    },
                           'is':{
                                    'friendly_name' : 'Equals',
                                    'widget'        : 'StringWidget',
                                    },
                           },
                  },
         'getId':{
                  'friendly_name': 'Short name',
                  'description': 'Short name of the item',
                  'operators':{
                           'is_not':{
                                    'friendly_name' : 'Does not equal',
                                    'widget'        : 'StringWidget',
                                    },
                           'is':{
                                    'friendly_name' : 'Equals',
                                    'widget'        : 'StringWidget',
                                    },
                           },
                  },
         'start':{
                  'friendly_name': 'Start date',
                  'description': 'The start date and time of an event',
                  'operators':{
                           'smaller_or_equal':{
                                    'friendly_name': 'Before',
                                    'widget': 'DateWidget',
                                    },
                          'is':{
                                    'friendly_name': 'On',
                                    'widget': 'DateWidget',
                                    },
                          'larger_then':{
                                    'friendly_name': 'After',
                                    'widget': 'DateWidget',
                                    },
                           'between':{
                                    'friendly_name': 'Between',
                                    'widget': 'DateRangeWidget',
                                    },
                           },

                  },
         'review_state':{
                  'friendly_name': 'State',
                  'description': 'An item\'s workflow state (e.g.published)',
                  'operators':{
                           'is_not':{
                                    'friendly_name' : 'Equals',
                                    'widget'        : 'SelectionWidget',
                                    },
                           },
                  },
         'Title':{
                  'friendly_name': 'Title',
                  'description': 'Title of the item',
                  'operators':{
                           'is_not':{
                                    'friendly_name' : 'Does not equal',
                                    'widget'        : 'StringWidget',
                                    },
                           'is':{
                                    'friendly_name' : 'Equals',
                                    'widget'        : 'StringWidget',},
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
#         'getId':{  
#                  'friendly_name' : 'Short name',
#                  'description' : 'The short name of the item',
#         },
# same as getId?
#         'id':{  
#                  'friendly_name' : 'ID',
#                  'description' : '',
#         },
# this is portal type, such as document (not page), topic (not collection)
#         'portal_type':{  
#                  'friendly_name' : '',
#                  'description' : '',
#         },
         'review_state':{  
                  'friendly_name' : 'State',
                  'description' : 'An item\'s workflow state (e.g.published)',
         },
         'sortable_title':{  
                  'friendly_name' : 'Title',
                  'description' : 'An item\'s title transformed for sorting',
         },
# Same as Modification Date?
#         'Date':{  
#                  'friendly_name' : 'Date',
#                  'description' : '',
#         },
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
#         'getRawRelatedItems':{  
#                  'friendly_name': 'Related to',
#                  'description': 'Find items related to the selected items',
#         },
         'relevence':{
                  'friendly_name' : 'Relevence',
                  'description' : 'Relevence',
         }
}
