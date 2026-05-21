from odoo import api, fields, models
from odoo import http
import requests


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def get_weather_data(self):
        """get weather data using OpenWeatherMap API"""
        icp_sudo = self.env['ir.config_parameter'].sudo()
        api_key = icp_sudo.get_param('res.config.settings.api_key')
        method = icp_sudo.get_param('res.config.settings.method')
        if api_key and method == 'use_lat_long':
            latitude = self.env.user.partner_latitude
            longitude = self.env.user.partner_longitude
            if api_key and latitude and longitude:
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={api_key}"
                response = requests.get(url)
                data = response.json()
            return data

        if api_key and method == 'use_place':
            city = self.env.user.city
            if api_key and city:
                url =f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
                response = requests.get(url)
                data = response.json()
            return data
