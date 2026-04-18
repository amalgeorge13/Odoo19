from odoo import fields,models,api

class CrmTeam(models.Model):
    _inherit = "crm.team"

    commission_plan_id = fields.Many2one('crm.commission',string="Commission Plan")
    total_commission_amount = fields.Float(string="Total Commission",compute="_compute_total_commission")

    @api.depends('commission_plan_id')
    def _compute_total_commission(self):
        for record in self:
            sale_orders = record.env['sale.order'].search([('team_id.id', '=', record.id)])
            amount = 0
            for sale_order in sale_orders:
                amount += sale_order[0].team_commission_amount
            record.total_commission_amount = amount