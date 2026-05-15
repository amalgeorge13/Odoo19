{
    'name': 'Weather Notification',
    'author': 'Amall',
    'sequence': 0,
    'license': 'LGPL-3',
    'version': '19.0.0.0.1',
    'category': 'Task',
    'application': True,
    'depends': [
        'base','base_setup','mail',],
    'data': [
    'views/res_config_settings_view.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'weather_notification/static/src/js/weather_view.js',
            'weather_notification/static/src/xml/weather_view.xml',
        ],
    },


}