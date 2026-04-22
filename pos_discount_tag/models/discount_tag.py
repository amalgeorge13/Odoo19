from odoo import api,fields,models

class ProductDiscountTag(models.Model):
    _name = 'product.discount.tag'
    _description = 'Product Discount Tag'
    _inherit = ['pos.load.mixin']

    name = fields.Integer(string='Percentage')
