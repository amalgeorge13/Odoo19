from odoo import fields,models

class RepairTags(models.Model):
    _name = "repair.tags"
    _description = "Repair Tags"
    _rec_name = 'tag_name'

    tag_name = fields.Char(string=" Tag Name",required=True)
    color=fields.Integer()