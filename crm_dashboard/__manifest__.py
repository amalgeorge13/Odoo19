{
    'name': 'CRM Dashboard',
    'author': 'Amall',
    'sequence': 0,
    'license': 'LGPL-3',
    'version': '19.0.1.1',
    'category': 'Task',
    'application': True,
    'depends': [
        'base','crm','sales_team','sale'],
    'data': [
    'views/crm_dashboard_view.xml',
    'views/crm_team_view.xml',
    'views/crm_dashboard_menu.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'crm_dashboard/static/src/js/dashboard.js',
            'crm_dashboard/static/src/xml/dashboard.xml',
            'https://cdn.jsdelivr.net/npm/chart.js'
        ],
    },


}