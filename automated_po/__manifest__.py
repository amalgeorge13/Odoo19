{
    'name': 'Automated PO',
    'author': 'Amall',
    'sequence': 1,
    'license': 'LGPL-3',
    'version': '19.0.1.1',
    'category': 'Purchase',
    'application': True,
    'depends': ['base','purchase'],
    'data': [
    'security/ir.model.access.csv',
    'views/product_product_views.xml',
    'views/purchase_order_wizard_view.xml',
    ]}