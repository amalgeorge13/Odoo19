from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def create_new_product(self, data):
        """
        get values from js and create new product record
        """
        name = data["product_name"]
        type = data["type"]
        price = data["price"]
        if name and type and price:
            self.create({
                "name": name,
                "type": type,
                "lst_price": float(price),
            })

    @api.model
    def edit_product(self, data,id):
        """
        get values from js and edit existing product record
        """
        rec=self.browse(id)

        if rec.lst_price!=data["price"] and data["price"]:
            rec.write({
                "lst_price": data["price"],
            })
        if rec.name!=data["product_name"] and data["product_name"]:
            rec.write({
                "name": data["product_name"],
            })
