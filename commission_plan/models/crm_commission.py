from odoo import fields, models, api

class CrmCommission(models.Model):
    _name = 'crm.commission'
    _description = 'CRM Commission'
    _rec_name = 'name'

    name = fields.Char(string='Name',required=True)
    active = fields.Boolean(string='Active', default=True)
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    type = fields.Selection([('product_wise', 'Product Wise'),('revenue_wise', 'Revenue Wise')],string='Type')
    mode = fields.Selection([('straight','Straight'),('graduated','Graduated')],string='Mode',default='straight')

    product_wise_ids = fields.One2many('product.wise', 'plan_id', string='Product Wise')

    revenue_wise_ids = fields.One2many('revenue.wise', 'plan_id', string='Product Wise')








