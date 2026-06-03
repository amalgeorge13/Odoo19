from odoo import api, fields, models,Command

class ProductProduct(models.Model):
    _inherit = "product.product"


    minimum_stock = fields.Float(string="Minimum Stock")
    preferred_vendor_id = fields.Many2one('res.partner', string="Preferred Vendor")
    auto_po = fields.Boolean(string="Auto purchase")

    # @api.depends('qty_available')
    # def check_and_create(self):
    #     if self.qty_available < self.minimum_stock and self.auto_po:
    #         qty=self.minimum_stock - self.qty_available
    #
    #         self.env['purchase.order'].create({
    #             'partner_id': self.preferred_vendor_id.id,
    #             'order_line': [
    #                 Command.create({
    #                     'product_id': self.ids[0],
    #                     'product_qty': qty,
    #                     'price_unit': self.standard_price,
    #                 })
    #             ]
    #         })
