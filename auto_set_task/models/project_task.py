from odoo import api, fields, models

class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.onchange('tag_ids')
    def _onchange_tag_ids(self):
        # self.user_ids=
        assignees=[]
        tags=[]
        if not assignees:
            self.user_ids = False
        for tag in self.tag_ids:
            tags.append(tag.name)
        print(tags)
        users=self.env['res.users'].search([('active','=',True)])
        for user in users:
            if user.category_ids:
                for tag in user.category_ids:
                    if tag.name in tags:
                        assignees.append(user.id)
                        print(assignees)
                        print(tag.name)
        self.user_ids = assignees

        @api.onchange('personal_stage_id')
        def onchange_stage_id(self):
            # if self.personal_stage_id == "01_in_progress":
                print(12345)