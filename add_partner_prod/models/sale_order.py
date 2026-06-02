from odoo import api, fields, models, Command
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    add_associated_products = fields.Boolean(string="Add Associated Products", default=False)

    @api.onchange('add_associated_products')
    def _onchange_add_associated_products(self):
        """
        if the add_associated_products is enabled add the associated products of the partner to the order line.
        if disable remove the products from order line
        """
        associated_products = self.partner_id.associated_product_ids
        associated_products_lines = []
        remove_associated_products_lines = []
        if self.add_associated_products:
            if self.partner_id and associated_products:
                for product in associated_products:
                    if product in self.order_line.product_id:
                        for line in self.order_line:
                            if line.product_id == product:
                                line.product_uom_qty += 1

                    else:
                        associated_products_lines.append(Command.create({
                            'product_id': product,
                            'product_uom_qty': 1,
                        }))
                self.order_line = associated_products_lines
        else:
            if self.partner_id and associated_products:
                for line in self.order_line:
                    if line.product_id in associated_products:
                        if line.product_uom_qty > 1:
                            line.product_uom_qty -= 1
                        else:
                            remove_associated_products_lines.append(Command.unlink(line.id))
                self.order_line = remove_associated_products_lines