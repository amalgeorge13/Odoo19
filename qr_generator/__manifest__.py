{
    'name': 'QR Generator',
    'author': 'Amall',
    'sequence': 0,
    'license': 'LGPL-3',
    'version': '19.0.0.0.1',
    'category': 'Task',
    'application': True,
    'depends': [
        'base','base_setup','mail','point_of_sale'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'qr_generator/static/src/js/qr_menu.js',
            'qr_generator/static/src/xml/qr_menu.xml',
            'qr_generator/static/src/js/qr_popup.js',
            'qr_generator/static/src/xml/qr_popup.xml',
        ],
    },


}