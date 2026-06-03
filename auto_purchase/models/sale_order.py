from odoo import api, fields, models,Command

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super().action_confirm()
        for line in self.order_line:
            product=line.product_id
            if product.auto_po:
                if product.qty_available and product.minimum_stock and product.preferred_vendor_id :
                    print(product.qty_available, product.minimum_stock, product.preferred_vendor_id)
                    if product.qty_available - line.product_uom_qty < product.minimum_stock:
                        qty = (product.minimum_stock -product.qty_available)+line.product_uom_qty
                        self.env['purchase.order'].create({
                            'partner_id': product.preferred_vendor_id.id,
                            'order_line': [
                                Command.create({
                                    'product_id': product.id,
                                    'product_qty': qty,
                                    'price_unit': product.standard_price,
                                })
                            ]
                        })

        return res
