from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    state=fields.Selection(selection_add = [('approve', 'To Approve'),('sale',)])

    def action_confirm(self):
        for order in self:
            if order.amount_total>1000:
                order.write({'state':'approve'})
                self.env.cr.commit() #for set state in db
                print(order.state)
                raise ValidationError("Restricted Amount")

        return super().action_confirm()

