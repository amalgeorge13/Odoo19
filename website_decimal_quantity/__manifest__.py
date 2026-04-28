{
    'name': 'Website Decimal Quantity',
    'author': 'Amall',
    'sequence': 0,
    'license': 'LGPL-3',
    'version': '19.0.1.1',
    'category': 'Website',
    'application': True,
    'depends': [
        'base','website_sale',],
    'data': [
    'views/website_sale_view.xml',

    ],
    'assets': {
        'web.assets_frontend': [
            'website_decimal_quantity/static/src/js/website_sale.js',
        ]
    }
}