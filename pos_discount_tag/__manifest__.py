{
    'name': 'Product Discount Tag',
    'author': 'Amall',
    'sequence': 2,
    'license': 'LGPL-3',
    'version': '19.0.1.1',
    'category': 'POS',
    'application': True,
    'depends': ['base','product','point_of_sale'],
    'data': [
    'security/ir.model.access.csv',
    'views/product_template_view.xml',

    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_discount_tag/static/src/xml/product_card.xml',
            'pos_discount_tag/static/src/xml/orderline.xml',
        ],
    }

}