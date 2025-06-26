{
    'name': 'estate', 
    'version': '1.0', 
    'description': 'a real estate app that lists properties, and allows buyers to place bids on them',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml'
    ],
    'application': True
}