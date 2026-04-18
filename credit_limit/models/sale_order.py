from odoo import fields, models,api

class SalesOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        customer_invoices = self.env['account.move'].search([
            # ('state', '=', 'posted'),
            ('payment_state','=','not_paid'),
            ('partner_id', '=', self.partner_id.id)
        ])

        due=0
        for i in customer_invoices:
            due += i.amount_residual

        if self.partner_id.warning_amount < due < self.partner_id.blocking_amount and self.partner_id.credit_limit_active == True:

            return {'warning': {
                'title': 'Warning',
                'message': f'Credit Limit Warning. \ndue amount : {due}',
            }}

        if due > self.partner_id.blocking_amount and self.partner_id.credit_limit_active == True:
            self.state = 'cancel'

            return {'warning': {
                'title': 'Blocked',
                'message': f'Due Amount Crossed Credit Limit. \ndue amount : {due}',
            }}

