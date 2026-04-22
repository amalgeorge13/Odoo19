from odoo import fields, models,api


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _description = "Product Template"

    discount_tag_id = fields.Many2one('product.discount.tag',string='Discount')
    orginal_price = fields.Float(string='Original Price',store=True)

    @api.onchange('discount_tag_id')
    def _onchange_discount_tag_id(self):
        """if set discount_tag_id, then set list price as dicounted amount"""
        if not self.orginal_price:
            self.orginal_price=self.list_price
        if self.discount_tag_id:
            self.list_price = self.orginal_price - (self.orginal_price * (self.discount_tag_id.name/100))
        else:
            self.list_price = self.orginal_price


    @api.model
    def _load_pos_data_fields(self, config_id):
        """
        Adds the 'product_owner_id' field to the list of fields loaded into the POS.
        """
        data = super()._load_pos_data_fields(config_id)
        data += ['discount_tag_id']
        print(data)
        return data
