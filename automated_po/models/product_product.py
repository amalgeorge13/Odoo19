from odoo import models, fields, api
class ProductProduct(models.Model):
    _inherit = "product.product"

    def create_purchase_order(self):
        return {'type': 'ir.actions.act_window',
                'name': 'Create Purchase Order',
                'res_model': 'purchase.order.wizard',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_product_id': self.id},
                }

