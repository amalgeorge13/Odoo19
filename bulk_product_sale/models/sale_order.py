from odoo import api, fields, models
from odoo import Command


class SaleOrder(models.Model):
    _inherit = "sale.order"

    product_ids = fields.Many2many('product.product', string="Products")
    quantity = fields.Integer(string="Quantity")

    def add_to_order_line(self):
        for product in self.product_ids:

            if self.quantity > 0:

                    if product in self.order_line.product_id:
                        for line in self.order_line:

                            if product.id == line.product_id.id:
                                line.product_uom_qty = line.product_uom_qty + self.quantity



                    else:
                        self.write({
                            "order_line" :[Command.create({
                                'product_id': product.id,
                                'product_uom_qty':self.quantity,
                            })
                            ]
                        })

        self.quantity = False
        self.product_ids = False


