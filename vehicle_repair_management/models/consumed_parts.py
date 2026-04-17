from odoo import fields, models, api


class ConsumedParts(models.Model):
    _name = "consumed.parts"
    _description = "Consumed Parts"
    _rec_name = "reference"

    reference = fields.Many2one('vehicle.repair',string="reff")
    part_id = fields.Many2one('product.product',string="Parts",domain=[('type','!=','service')])
    quantity = fields.Float(string="Quantity")
    unit_price = fields.Float(related='part_id.list_price',string="Price")
    amount = fields.Float(string="Amount",compute="_compute_amount")

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for record in self:
            record.amount = record.quantity * record.unit_price
