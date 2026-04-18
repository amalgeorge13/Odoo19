from odoo import fields, models, api

class RevenueWise(models.Model):
    _name = 'revenue.wise'

    plan_id = fields.Many2one('crm.commission',string='Plan')
    sequence =fields.Integer(string='Sequence')
    from_amount = fields.Float(string='From Amount')
    to_amount = fields.Float(string='To Amount')
    rate = fields.Float(string='Rate')