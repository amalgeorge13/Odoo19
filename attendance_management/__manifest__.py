{
    'name': 'Attendance Management',
    'author': 'Amall',
    'sequence': 0,
    'license': 'LGPL-3',
    'version': '19.0.1.1',
    'category': 'Attendance',
    'application': True,
    'depends': [
        'base','hr'],
    'data': [
    'security/ir.model.access.csv',
    'data/ir_cron.xml',
    'views/absentees_views.xml',
    'views/attendance_management_menu.xml',

    ]}