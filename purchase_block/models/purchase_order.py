from odoo import api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        res = super().button_confirm()
        today = fields.Date.today()
        if self.partner_id.last_reference_date:
            if self.partner_id.last_reference_date < today - relativedelta(days=90):
                raise ValidationError("Purchase blocked. vendor hasn’t supplied anything for more than 90 days")
        self.partner_id.last_reference_date = today
        return res

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        today = fields.Date.today()
        if self.partner_id.last_reference_date:
            if self.partner_id.last_reference_date < today - relativedelta(days=90):
                return {'warning': {
                    'title': 'Warning',
                    'message': 'Vendor has Overdue'
                }}


