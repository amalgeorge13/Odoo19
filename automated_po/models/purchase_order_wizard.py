from odoo import api, fields, models,Command

class PurchaseOrderWizard(models.TransientModel):
    _name = "purchase.order.wizard"
    _description = "Purchase Order Wizard"


    product_id = fields.Many2one('product.product',string="Product")
    partner_id = fields.Many2one('res.partner', string="Vendor",required=True)
    quantity = fields.Float(string="Quantity")
    price = fields.Float(string="Price")

    @api.onchange('product_id')
    def onchange_seller_ids(self):
        """set partner_id"""
        if self.product_id.seller_ids:
            self.partner_id = self.product_id.seller_ids[0].partner_id
        else:
            self.partner_id = False

    def confirm_po(self):
        """Create and Confirm the purchase order"""
        self.env['purchase.order'].create({
            'partner_id': self.partner_id.id,
            'state': 'draft',
            'order_line': [
                Command.create({
                    'product_id': self.product_id.id,
                    'product_qty': self.quantity,
                    'price_unit': self.price,
                })
            ]
        }).button_confirm()