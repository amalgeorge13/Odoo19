from odoo import api, fields, models
from odoo import http
import requests


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def get_weather_data(self):
        icp_sudo = self.env['ir.config_parameter'].sudo()
        api_key = icp_sudo.get_param('res.config.settings.api_key')
        use_lat_long=icp_sudo.get_param('res.config.settings.use_lat_long')
        lat=icp_sudo.get_param('res.config.settings.latitude')
        lon=icp_sudo.get_param('res.config.settings.longitude')
        print(api_key, lat, lon)
        if api_key and use_lat_long:
            latitude=lat
            longitude=lon
            print(34567890)
        else:
            latitude=self.env.user.partner_latitude
            longitude=self.env.user.partner_longitude

        if api_key and latitude and longitude:
            url=f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={api_key}"
            response = requests.get(url)
            data = response.json()
            print(data)

        return data