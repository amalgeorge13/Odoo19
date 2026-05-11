{
    'name': 'Payment Provider: Multisafepay',
    'author': 'Amall',
    'sequence': 5,
    'license': 'LGPL-3',
    'version': '19.0.1.1',
    'category': 'Integration',
    'application': True,
    'depends': [
        'base','payment'],
    'data': [
        'data/payment_provider_data.xml',
        'data/payment_method_data.xml',
        'views/payment_provider_view.xml',
        'views/payment_multisafepay_templates.xml',

    ]}