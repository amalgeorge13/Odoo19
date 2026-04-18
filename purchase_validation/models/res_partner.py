
from odoo import fields, models,api

class ResPartner(models.Model):
    _inherit = 'res.partner'


    restricted=fields.Boolean(string="Restricted")
    restricted_count=fields.Integer(string="Restricted Count")

    def action_shop(self):
        return {'type': 'ir.actions.act_window',
                'name': 'Shop',
                'res_model': 'bulk.price',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_user_id': self.id}, }



