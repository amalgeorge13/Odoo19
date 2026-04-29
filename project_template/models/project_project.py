from odoo import api, fields, models
from odoo import Command

class ProjectProject(models.Model):
    _inherit = 'project.project'

    def create_template(self):
        """ Create Project Template """
        tasks = []
        if self.task_ids:
            for task in self.task_ids:
                tasks.append(Command.create({
                    'task_name': task.name,
                    'user_ids': task.user_ids.ids,
                    'date_deadline': task.date_deadline
                }))
        self.env['project.template'].create({
            'name':self.name,
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'tag_ids': self.tag_ids.ids,
            'task_ids': tasks,
        })