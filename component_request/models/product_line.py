from odoo import api, fields, models

class ProductLine(models.Model):
    _name = 'product.line'
    _description = 'Product Line'

    request_id = fields.Many2one(comodel_name='product.request',string='Loan Line')
    product_id = fields.Many2one(comodel_name='product.product',string='Product')
    quantity = fields.Float(string='Quantity')
    operation_type_id = fields.Many2one('stock.picking.type',string='Operation Type')