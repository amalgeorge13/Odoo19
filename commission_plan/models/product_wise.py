from odoo import fields, models, api

class ProductWise(models.Model):
    _name = 'product.wise'

    plan_id = fields.Many2one('crm.commission',string='Plan')
    product_category_id = fields.Many2one('product.category',string="Product Category")
    product_name_id = fields.Many2one('product.product',string="Product Name",domain="[('categ_id','=',product_category_id)]")
    rate = fields.Float(string="Rate")
    max_commission_amount = fields.Float(string="Max Commission Amount")