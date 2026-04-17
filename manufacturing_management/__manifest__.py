{
    'name': 'Manufacturing Management',
    'author': 'Amall',
    'sequence': 0,
    'license': 'LGPL-3',
    'version': '19.0.1.1',
    'category': 'Manufacturing',
    'application': True,
    'depends': ['base','product','mrp'],
    'data': [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/mrp_production_ext.xml',
        'views/mrp_production_material_line_views.xml',
        'views/manufacturing_management_menu.xml',
    ]


}