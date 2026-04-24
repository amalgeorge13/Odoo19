{
    'name': 'Product Qty',
    'author': 'Amall',
    'sequence': 2,
    'license': 'LGPL-3',
    'version': '19.0.1.1',
    'category': 'POS',
    'application': True,
    'depends': ['base','product','point_of_sale','stock'],
    'data': [
        'views/res_config_settings.xml',
        # 'views/product_template_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_product_qty/static/src/js/product_card.js',
            # 'pos_product_qty/static/src/xml/product_card.xml',
        ],
    }

}