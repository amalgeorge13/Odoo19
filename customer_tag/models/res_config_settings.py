from ast import literal_eval
from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    """Extension of 'res.config.settings' for configuring delivery settings."""
    _inherit = 'res.config.settings'


    tags = fields.Many2many('res.partner.category',string='Tags',
                                        help='Set Allowed Customer/Vendor Tags')
    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        tags = icp_sudo.get_param('res.config.settings.tags')
        res.update(
            tags=[(6, 0, literal_eval(tags))] if tags else False,
        )
        return res
    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.tags',self.tags.ids)
        return res
