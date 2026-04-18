from odoo import api, fields, models

class BulkPrice(models.TransientModel):
    _name = "bulk.price"
    _description = "Bulk Price"
    product_id = fields.Many2many('product.product', string="Product")
    price_based = fields.Selection([('percentage','Percentage'),('fixed_price','Fixed Price')],string="Based On")
    percentage = fields.Float(string="Percentage")
    fixed_price = fields.Float(string="Fixed Price")
    summary = fields.Text(string="Summary")

    def update_price(self):
        updated=''
        for product in self.product_id:
            if self.price_based:
                if self.price_based == 'percentage':
                    new_price = product.lst_price + (self.percentage/100) * product.lst_price
                    print(new_price)
                    product.write({'lst_price': new_price})
                else:
                    new_price = product.lst_price + self.fixed_price
                    product.write({'lst_price': new_price})
                    print(new_price)
                updated = updated + product.name +"->"+ str(new_price)+","
        self.summary=updated
        return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Price Update!',
                    'message': f'Products price changed their new prices: \n{self.summary}',
                    'type': 'success',
                    'sticky': True
                }
            }

