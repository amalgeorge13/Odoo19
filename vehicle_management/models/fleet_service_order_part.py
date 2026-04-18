from odoo import fields, models, api


class FleetServiceOrderPart(models.Model):
    _name = 'fleet.service.order.part'

    order_id = fields.Many2one('fleet.service.order')
    product_id = fields.Many2one('product.product')
    quantity = fields.Float(string='Quantity')
    unit_price = fields.Float(string='Unit Price')
    amount = fields.Float(string='Amount',compute='_compute_amount')

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for record in self:
            record.amount = record.quantity * record.unit_price

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.unit_price =self.product_id.lst_price