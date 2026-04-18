from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    restricted = fields.Boolean(related="partner_id.restricted")
    restricted_count = fields.Integer(related="partner_id.restricted_count")

    @api.constrains("order_line")
    def check_order_length(self):
        for order in self:
            if order.restricted and order.restricted_count > 0:
                if len(order.order_line) > order.restricted_count:
                    raise ValidationError("Restricted Order Length")


