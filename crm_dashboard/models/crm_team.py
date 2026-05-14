from odoo import models, api, fields


class CrmTeam(models.Model):
    _inherit = "crm.team"

    stage_id = fields.Many2one('crm.stage',string="Stage")