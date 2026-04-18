{
    'name': 'Commission Plan',
    'author': 'Amall',
    'sequence': 1,
    'license': 'LGPL-3',
    'version': '19.0.1.1',
    'category': 'Task',
    'application': True,
    'depends': [
        'base','product','sales_team','sale'],
    'data': [
    'security/ir.model.access.csv',
    'views/crm_commission_views.xml',
    'views/product_wise_views.xml',
    'views/revenue_wise_views.xml',
    'views/crm_team_views.xml',
    'views/res_users_views.xml',
    'views/sale_order_views.xml',
    'views/commission_plan_menu.xml',

    ]}