from odoo import fields, models, api
from collections import Counter

class SaleInfo(models.Model):
    _name = 'sale.info'
    _description = 'Sale Information'
    _rec_name = 'sale_order_id'


    sale_order_id = fields.Many2one('sale.order',string='Sale Order',required=True)
    name = fields.Char(string='Name',readonly=True,store=False,index=False)
    names = fields.Char(store=True)

    def button_click(self):
        print(self)
        print("\nCustomer name: ",self.sale_order_id.partner_id.name)
        partner=self.sale_order_id.partner_id
        print("\nCountry: ",self.sale_order_id.partner_id.country_id.name)
        print("\nCurrency",self.sale_order_id.partner_id.currency_id.name)
        print("\nSale Orders: ",self.sale_order_id.partner_id.sale_order_count)

        all = self.env["sale.order"].search([('partner_id', '=', partner)])
        total=0
        total_margin=0
        products=[]
        price_of_product = {}
        purchase_linked=[]
        for order in all:
            total=total+order.amount_total
            if order.purchase_order_count>0:
                purchase_linked.append(order.name)
            for p in order.order_line:
                name=p.product_id.name
                price=p.product_id.lst_price
                total_margin=total_margin+p.margin
                qty=int(p.product_uom_qty)
                if qty>0:
                    price_of_product[name] = price_of_product.get(name, 0) + price * qty
                    for i in range(qty):
                        products.append(name)
        print("\nTotal Amount Spend: ",total)
        print("\nproducts :",products)
        products_with_count = Counter(products)
        print("\nProducts With Count :",products_with_count)
        max_product_count=max(products_with_count,key=products_with_count.get)
        print("\nMost Buy Product :",max_product_count)
        min_product_count=min(products_with_count,key=products_with_count.get)
        print("\nLeast Buy Product :",min_product_count)
        print("\nTotal Margin :",total_margin)
        print(price_of_product)
        max_product_price=max(price_of_product,key=price_of_product.get)
        print("\nMost Purchased Product by Value :",max_product_price)
        min_product_price=min(price_of_product,key=price_of_product.get)
        print("\nLeast Purchased Product by Value :",min_product_price)
        print("\nCustomer Sale orders that linked with purchase order :",purchase_linked)





