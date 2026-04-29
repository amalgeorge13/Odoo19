from odoo import api, fields, models

class ProjectTask(models.Model):
    _inherit = 'project.task'
    _description = 'Project Task'

    def create_task_template(self):
        """Creating Task Template"""
        self.env['task.template'].create({
            'task_name': self.name,
            'user_ids': self.user_ids.ids,
            'date_deadline': self.date_deadline
        })