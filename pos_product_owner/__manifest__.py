{
    'name': 'Product Owner',
    'author': 'Amall',
    'sequence': 2,
    'license': 'LGPL-3',
    'version': '19.0.1.1',
    'category': 'POS',
    'application': True,
    'depends': ['base','product','point_of_sale'],
    'data': [
    'views/product_product_view.xml',

    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_product_owner/static/src/js/orderline.js',
            'pos_product_owner/static/src/xml/pos_screen.xml',
        ],
    }

}