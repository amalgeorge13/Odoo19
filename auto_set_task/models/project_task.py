from odoo import api, fields, models

class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.onchange('tag_ids')
    def _onchange_tag_ids(self):
        # self.user_ids=
        tags=[]
        for tag in self.tag_ids:
            tags.append(tag.name)
        print(tags)
        # users=self.env['res.users'].search([('category_ids','=',True)])
        # print(users)



        # print(self.env['res.users'].search([('category_ids','=',True)]))
