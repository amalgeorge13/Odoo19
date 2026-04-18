
from odoo import fields, models,api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    most_sold_product = fields.Many2one('product.product',string="Most Sold Product",compute="_compute_details")
    total_sold_quantity = fields.Float(string="Total Sold Quantity")
    minimum_sold_price = fields.Float(string="Minimum Sold Price")
    maximum_sold_price = fields.Float(string="Maximum Sold Price")
    sale_order_counts = fields.Integer(string="Sale Order Count",default=0)


    def _compute_details(self):
        """find max sold product,product count,minimum sold price,maximum sold price"""
        partner_products = self.env['sale.order'].search([('partner_id','=',self.id)])
        product_count ={}
        prices=[]
        self.sale_order_counts=0
        for rec in partner_products.order_line:
            product_count[rec.product_id] = product_count.get(rec.product_id, 0) + rec.product_uom_qty
        max_product_count= max(product_count, key=product_count.get)
        self.most_sold_product = max_product_count
        self.total_sold_quantity = product_count[max_product_count]

        for rec in partner_products.order_line:
            if rec.product_id == max_product_count and rec.product_uom_qty > 0:
                prices.append(rec.price_unit)
                self.sale_order_counts += 1

        self.minimum_sold_price = min(prices)
        self.maximum_sold_price = max(prices)

    def fetch_sale_orders(self):
        """fetch sale orders"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'sale_orders',
            'view_mode': 'list,form',
            'res_model': 'sale.order',
            'domain': [('partner_id', '=', self.id),('order_line', 'any', [('product_id', '=', self.most_sold_product.id),])],
            'context': {'create': False},
        }




