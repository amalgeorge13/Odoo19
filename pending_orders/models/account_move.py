from odoo import api, fields, models
from odoo import Command

class AccountMove(models.Model):
    _inherit = "account.move"

    pending_order_ids = fields.Many2many('sale.order', string="Pending Orders",domain=[('invoice_status','=','to invoice')])

    @api.onchange('pending_order_ids')
    def onchange_pending_order_ids(self):
        self.invoice_line_ids = [Command.clear()]
        order_lines = []

        for order in self.pending_order_ids:
            for line in order.order_line:
                order_lines.append(Command.create({
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'quantity': line.qty_to_invoice,
                    'price_unit': line.price_unit
                }))

        self.invoice_line_ids = order_lines


