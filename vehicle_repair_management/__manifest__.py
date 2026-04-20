{
    'name': 'Vehicle Repair',
    'author': 'Amal',
    'sequence': 0,
    'license': 'LGPL-3',
    'version': '19.0.1.0',
    'category': 'Management',
    'application': True,
    'depends': [
        'base','fleet','mail','hr','sale','account','website','portal'],
    'data': [
    'security/vehicle_repair_security.xml',
    'security/ir.model.access.csv',
    'report/repair_report_views.xml',
    'report/report_template.xml',
    'data/ir_sequence_data.xml',
    'data/fleet_category_demo.xml',
    'data/product_demo.xml',
    'data/mail_template_data.xml',
    'data/ir_cron.xml',
    'views/snippets/repair_template.xml',
    'views/vehicle_repair_views.xml',
    'views/repair_tags_views.xml',
    'views/consumed_parts_views.xml',
    'views/labor_cost_views.xml',
    'views/res_partner_views.xml',
    'views/wizard_report_views.xml',
    'views/website_repair_request.xml',
    'views/repair_request_template.xml',
    'views/vr_portal_templates.xml',
    'views/vehicle_repair_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'vehicle_repair_management/static/src/js/action_manager.js',
        ],
        'web.assets_frontend': [
            'vehicle_repair_management/static/src/xml/repair_highlight_content.xml',
            'vehicle_repair_management/static/src/js/vehicle_repair.js',
        ]
    }
}