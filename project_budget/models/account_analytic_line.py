from odoo import fields, models, api

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    cost= fields.Float(string='Cost',compute='_compute_cost')

    @api.depends('unit_amount')
    def _compute_cost(self):
        self.cost= self.unit_amount * self.employee_id.hourly_cost
