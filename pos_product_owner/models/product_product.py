from odoo import fields, models,api


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Product Product'

    product_owner_id = fields.Many2one('res.partner',string='Product Owner')

    @api.model
    def _load_pos_data_fields(self, config_id):
        """
        Adds the 'product_owner_id' field to the list of fields loaded into the POS.
        """
        data = super()._load_pos_data_fields(config_id)
        data += ['product_owner_id']
        return data