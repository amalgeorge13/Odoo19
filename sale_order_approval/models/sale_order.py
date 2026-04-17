
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    state=fields.Selection(selection_add = [('approve1', 'Approve'),('approve2', 'Approve'),('sale',)])
    approved=fields.Boolean(default=False,copy=False)


    def action_confirm(self):
        amount = self.env['ir.config_parameter'].sudo().get_param('res.config.settings.amount')
        """if amount total more than amount limit state changes to approval"""
        for order in self:
            if order.amount_total > float(amount) and order.approved == False:
                order.state = 'approve1'
                self.approved = True
            else:
                order.state = 'draft'
                return super().action_confirm()


    def first_approval(self):
        """state change to 2nd approval"""
        self.state = 'approve2'

    def second_approval(self):
        """state change to sale order"""
        self.action_confirm()
