{
    'name': 'Sale Order Approval',
    'author': 'Amall',
    'sequence': 2,
    'license': 'LGPL-3',
    'version': '19.0.1.1',
    'category': 'Sales Management',
    'application': True,
    'depends': ['base','sale'],
    'data': [
    'security/sale_approve_security.xml',
    'views/sale_order_view.xml',
    'views/res_config_settings.xml',

    ]}