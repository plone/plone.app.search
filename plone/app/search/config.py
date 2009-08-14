

CRITERION={
    'indexes': [
        {'name': 'Creator',
         'friendly_name': 'Creator',
         'operators': [
            {'name': 'is_not',
             'friendly_name': 'Does not equal',
             'widget': 'StringWidget',},
            {'name': 'is',
             'friendly_name': 'Equals',
             'widget': 'StringWidget',},
        ],},
        {'name': 'modified',
         'friendly_name': 'Modification date',
         'operators': [
            {'name': 'smaller_or_equal',
             'friendly_name': 'Before',
             'widget': 'DateWidget',},
            {'name': 'is',
             'friendly_name': 'On',
             'widget': 'DateWidget',},
            {'name': 'larger_then',
             'friendly_name': 'After',
             'widget': 'DateWidget',},
            {'name': 'between',
             'friendly_name': 'between',
             'widget': 'DateWidget',},
        ],},
    ],
}