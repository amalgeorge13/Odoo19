from flake8.formatting import default

from odoo import api, fields, models,Command

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    created_from =fields.Integer("Created from")

    def button_confirm(self):
        res = super().button_confirm()
        this=self.id
        print(this)
        vendor=[]
        non_seller_order_line = []
        for line in self.order_line:
            if line.product_id.seller_ids:
                self.button_cancel()
                minimum = min(line.product_id.seller_ids, key=lambda l: l.price)
                print(minimum.partner_id,minimum.price)
                if minimum.partner_id not in vendor:
                    seller_order_line=[
                        Command.create({
                            'product_id': line.product_id.id,
                            'product_qty': line.product_qty,
                            'price_unit': minimum.price,
                        })]
                    vendor.append(minimum.partner_id)
                    self.env['purchase.order'].create({
                    'partner_id': minimum.partner_id.id,
                    'state': 'draft',
                    'order_line': seller_order_line,
                    'created_from': this,
                    })
                else:
                    PO=self.env['purchase.order'].search([('state', '=', 'draft'),('partner_id', '=',minimum.partner_id)],
                                                      limit=1,order='name desc')


                    if line.product_id in PO.product_id:
                        for po_line in PO.order_line:
                            if po_line.product_id == line.product_id:
                                po_line.product_qty = po_line.product_qty+line.product_qty


                    else:
                        self.env['purchase.order.line'].create({
                            'order_id':PO.id,
                            'product_id': line.product_id.id,
                            'product_qty': line.product_qty,
                            'price_unit': minimum.price,

                        })

            else:
                non_seller_order_line.append(Command.create({
                    'product_id': line.product_id.id,
                    'product_qty': line.product_qty,
                }))

        if non_seller_order_line:
            self.env['purchase.order'].create({
                'partner_id': self.partner_id.id,
                'state': 'draft',
                'created_from': this,
                'order_line': non_seller_order_line
            })

        return res

    def purchase_orders(self):
        print(self.id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Orders',
            'view_mode': 'list,form',
            'res_model': 'purchase.order',
            'domain': [('created_from', '=', self.id)],
            'context': {'create': False},
        }