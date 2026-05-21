from odoo import api, fields, models
from odoo import http
import requests


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_key = fields.Char(string="API Key")
    method = fields.Selection([('use_lat_long', 'Use  User Latitude Longitude'),('use_place', 'Use User Place')],default='use_lat_long')

    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        api_key = icp_sudo.get_param('res.config.settings.api_key')
        method = icp_sudo.get_param('res.config.settings.method')

        res.update(
            api_key=api_key if api_key else False,
            method=method if method else False,
        )
        return res

    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.api_key', self.api_key)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.method', self.method)

        return res