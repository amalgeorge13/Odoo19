from odoo import api,fields,models

class ResUsers(models.Model):
    _inherit = "res.users"

    commi_plan_id = fields.Many2one('crm.commission',string="Commission Plan")
    total_commission_amount = fields.Float(string="Total Commission",compute="_compute_total_commission")

    @api.depends('commi_plan_id')
    def _compute_total_commission(self):
        for record in self:
            sale_orders = record.env['sale.order'].search([('user_id','=',record.id)])
            amount = 0
            for sale_order in sale_orders:
                amount += sale_order[0].person_commission_amount
            record.total_commission_amount = amount
