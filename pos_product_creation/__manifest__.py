{
    'name': 'Product Creation',
    'author': 'Amall',
    'sequence': 2,
    'license': 'LGPL-3',
    'version': '19.0.1.1',
    'category': 'POS',
    'application': True,
    'depends': ['base','point_of_sale'],
    'data': [
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_product_creation/static/src/js/control_buttons.js',
            # 'pos_product_creation/static/src/js/product_button_popup.js',
            'pos_product_creation/static/src/xml/control_buttons.xml',
            # 'pos_product_creation/static/src/xml/product_button_popup.xml',

        ],
    }
}