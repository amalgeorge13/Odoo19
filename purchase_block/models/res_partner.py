
from odoo import fields, models,api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    last_reference_date=fields.Date(string="Last Reference Date")





