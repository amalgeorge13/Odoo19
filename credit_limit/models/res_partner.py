from odoo import fields, models,api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_limit_active = fields.Boolean(string="Active Credit Limit", default=False)
    warning_amount=fields.Float(string="Warning Amount",default=0)
    blocking_amount=fields.Float(string="Blocking Amount",default=0)

    def enable_credit_limit(self):
        self.credit_limit_active = True

    def disable_credit_limit(self):
        self.credit_limit_active = False
        self.warning_amount = False
        self.blocking_amount = False

