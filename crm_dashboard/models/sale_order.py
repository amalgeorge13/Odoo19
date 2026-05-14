from odoo import api,fields,models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """when confirming sale order set the stage id of opportunity"""
        res = super().action_confirm()
        if self.team_id.stage_id and self.opportunity_id:
            self.opportunity_id.stage_id=self.team_id.stage_id
        return res