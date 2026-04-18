{
    'name': 'Purchase Validation',
    'author': 'Amall',
    'sequence': 2,
    'license': 'LGPL-3',
    'version': '19.0.1.1',
    'category': 'Purchase',
    'application': True,
    'depends': ['base','purchase'],
    'data': [
    'security/ir.model.access.csv',
    'security/bulk_price_security.xml',
    'views/res_partner_views.xml',
    'views/purchase_order_views.xml',
    'views/bulk_price_views.xml'
    ]}