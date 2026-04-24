from odoo import fields,models,api
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    # _inherit = "res.config.settings"
    _inherit = ['pos.load.mixin','res.config.settings']

    location_id=fields.Many2one('stock.location',string="Location")

    @api.model
    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'testing_settings.location_id',
            self.location_id.id or False
        )

    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        value = self.env['ir.config_parameter'].sudo().get_param(
            'testing_settings.location_id'
        )
        res.update(location_id=literal_eval(value) if value else False)
        return res

    @api.model
    def _load_pos_data_fields(self, config_id):
        """
        Adds the 'product_owner_id' field to the list of fields loaded into the POS.
        """
        data = super()._load_pos_data_fields(config_id)
        data += ['location_id']
        print(data)
        return data

    # @api.onchange('location_id')
    # def onchange_location_id(self):
    #     prod=self.env['product.template'].search([])
    #     prod.write({'loc_id':self.location_id.id})