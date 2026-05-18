from odoo import api, fields, models
from odoo import http
import requests


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_key = fields.Char(string="API Key")
    use_lat_long = fields.Boolean(default=False,string="Give Latitude and Longitude")
    latitude = fields.Float(string="Latitude")
    longitude = fields.Float(string="Longitude")

    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        api_key = icp_sudo.get_param('res.config.settings.api_key')
        use_lat_long = icp_sudo.get_param('res.config.settings.use_lat_long')
        latitude = icp_sudo.get_param('res.config.settings.latitude')
        longitude = icp_sudo.get_param('res.config.settings.longitude')
        res.update(
            api_key=api_key if api_key else False,
            use_lat_long=use_lat_long if use_lat_long else False,
            latitude=latitude if latitude and use_lat_long else False,
            longitude=longitude if longitude and use_lat_long else False,
        )
        return res

    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.api_key', self.api_key)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.use_lat_long', self.use_lat_long)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.latitude', self.latitude)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.longitude', self.longitude)
        return res

    def get_weather_data(self):
        print(1234567890)
    #     url = f"https://api.openweathermap.org/data/2.5/weather?lat=11.258753&lon=75.780411&units=metric&appid=8cf47f3abef0c4474f56081fb1d7a2dd"
        return 1

