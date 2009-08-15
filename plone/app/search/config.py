# Static config, for prototype use now.
# This have to be in the registry later on.
# For now its static

CRITERION={
         'Subject':{
                  'friendly_name': 'Subject',
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
                  },
         'path':{
                  'friendly_name': 'Location (path)',
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
                  'friendly_name': 'Is related',
                  'operators':{
                           'to':{
                                    'friendly_name' : 'to',
                                    'widget'        : 'MultipleSelectionWidget',
                                    },
                           },
                  },
         'SearchableText':{
                  'friendly_name': 'Search text',
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
                  'operators':{
                           'is_not':{
                                    'friendly_name' : 'Equals',
                                    'widget'        : 'SelectionWidget',
                                    },
                           },
                  },
         'Title':{
                  'friendly_name': 'Title',
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


#StringWidget
#DateWidget
#MultipleSelectionWidget
#ReferenceWidget
#RelativePathWidget
#DateRangeWidget
#IntegerWidget
#RangeWidget


