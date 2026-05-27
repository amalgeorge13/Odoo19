{
    'name': 'Product Creation',
    'version': "19.0.1.0.0",
    'description': '''
   This module adds a products button to POS that opens a Products screen.
   ''',
    'category': 'Point of Sale',
    'author': 'Amal',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'depends': ['base', 'mail','point_of_sale'],
    'data': [
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_product_creation/static/src/js/control_buttons.js',
            'pos_product_creation/static/src/xml/control_buttons.xml',
            'pos_product_creation/static/src/js/products_popup.js',
            'pos_product_creation/static/src/xml/products_popup.xml',
        ],
    },
}
