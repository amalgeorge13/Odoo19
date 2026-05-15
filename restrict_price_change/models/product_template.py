from odoo import models, api, fields
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_price_update = fields.Date(string="Last Update")

    @api.onchange('list_price')
    def _onchange_list_price(self):
        """
        Only Manger can change the price of products
        When Changing list price get the past sale prices calculating average
        if the changing price is less than the 80% of the average price raise validation error
        if passes validation set the date to last price update date
        """

        record_id = self.env.ref('sales_team.group_sale_manager').id
        if record_id not in self.env.user.group_ids.ids:
            raise ValidationError("Price change not allowed for this user")
        today = fields.Date.today()
        min_date=today - relativedelta(months=1)

        past_prices= self.env['sale.order.line'].search([('state','=','sale'),
                        ('product_id','=',self.product_variant_ids.ids),('create_date','>',min_date)]).mapped('price_unit')
        print(past_prices)
        avg_price=sum(past_prices) / len(past_prices)
        print(avg_price)
        min_price=avg_price*80/100
        if self.list_price < min_price:
            raise ValidationError("This Amount Lesser Than Minimum")
        self.last_price_update = today


