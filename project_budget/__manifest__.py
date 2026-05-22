{
    'name': 'Project Budget',
    'author': 'Amal',
    'sequence': 0,
    'license': 'LGPL-3',
    'version': '19.0.1.0',
    'category': 'Project',
    'application': True,
    'depends': [
        'base','project','mail','hr_timesheet','analytic'],
    'data': [
    'data/mail_template_data.xml',
    'views/project_project_view.xml',
    'views/project_task_view.xml',
    ],
}