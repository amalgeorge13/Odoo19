from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"


    delivery_remark = fields.Char(string="Delivery Remark")
    is_urgent_delivery = fields.Boolean(string="Is Urgent Delivery")
    preferred_delivery_time = fields.Selection([('morning','Morning'),('afternoon','Afternoon'),('evening','Evening')]
                                              ,string="Preferred Delivery Time")
    discount_approved = fields.Boolean(string="Discount Approved",copy=False)
    discount_approved_by = fields.Many2one('res.users',string="Discount Approved by User",readonly=True,tracking=True,copy=False)


    def approve_discount(self):
        """Approve discount button with validation"""
        if len(self.order_line) == 0:
            raise ValidationError("No order Lines")
        count=0

        for order in self.order_line:
            if order.discount :
                count = count + 1

        print(count)
        if count > 0:
            self.discount_approved = True
            self.discount_approved_by = self.env.user.id
            return self.message_post(body=f'Discount Approved {self.discount_approved_by.name}')


        else:
            raise ValidationError("OrderLine haven't discount yet.")




