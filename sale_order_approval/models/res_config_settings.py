from odoo import fields,models,api

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    amount = fields.Float(string="Amount Limit",default=0)

    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        amount = icp_sudo.get_param('res.config.settings.amount')
        res.update(
            amount=amount if amount else 0,
        )
        return res

    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.amount', self.amount)
        print(self.amount)
        return res