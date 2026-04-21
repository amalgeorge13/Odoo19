from ast import literal_eval
from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    tags = fields.Many2many('res.partner.category', string='Tags',readonly=True)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """get tags of allowed partner"""
        tag_ids = self.env['ir.config_parameter'].sudo().get_param('res.config.settings.tags')
        tag_ids = literal_eval(tag_ids)
        if tag_ids:
            self.tags = tag_ids
        else:
            self.tags = []

