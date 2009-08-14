

CRITERION={
         'Creator':{
            'friendly_name': 'Creator',
            'operators': {'is_not':
                            {'friendly_name' : 'Does not equal',
                            'widget'        : 'StringWidget',},
                            
                          'is':{
                            'friendly_name' : 'Equals',
                            'widget'        : 'StringWidget',},
                            },
                            
                            
         'modified':{
            'friendly_name': 'Modification date',
            'operators': {'smaller_or_equal':
                                {'friendly_name': 'Before',
                                'widget': 'DateWidget',},
                          'is':
                                {'friendly_name': 'On',
                            'widget': 'DateWidget',},
                          'larger_then':
                                {'friendly_name': 'After',
                                 'widget': 'DateWidget',},
                                 }
                    }
                }
            }