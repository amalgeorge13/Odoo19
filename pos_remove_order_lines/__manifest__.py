{
    'name': 'Remove Order Lines',
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
            'pos_remove_order_lines/static/src/js/action_pad_widget.js',
            'pos_remove_order_lines/static/src/js/control_buttons.js',
            'pos_remove_order_lines/static/src/js/order_line.js',
            'pos_remove_order_lines/static/src/xml/action_pad_widget.xml',
            'pos_remove_order_lines/static/src/xml/control_buttons.xml',
            'pos_remove_order_lines/static/src/xml/order_line.xml',

        ],
    }
}