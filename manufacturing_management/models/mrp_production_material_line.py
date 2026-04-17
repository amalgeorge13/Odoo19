# -*- coding: utf-8 -*-
from odoo import fields, models,api

class MrpProductionMaterialLine(models.Model):
    """Handling Mrp Production Material Line"""
    _name = 'mrp.production.material.line'
    _description = 'Mrp Production Material Line'

    production_id =fields.Many2one('mrp.production.ext', string='Production')
    product_id = fields.Many2one('product.product', string='Product')
    required_qty = fields.Float(string='Required Qty')
    available_qty = fields.Float(string='Available Qty')
    consumed_qty = fields.Float(string='Consumed Qty',readonly=True)
    remaining_qty = fields.Float(string='Remaining Qty',readonly=True)
