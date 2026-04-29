from odoo import api, fields, models

class TaskTemplate(models.Model):
    _name = 'task.template'
    _description = 'Task Template'
    _rec_name = 'task_name'

    task_name = fields.Char(string="Task",required=True)
    user_ids = fields.Many2many('res.users', string="Assignees")
    date_deadline = fields.Date(string="Deadline")

    def create_task(self):
        """Creating Task"""
        self.env['project.task'].create({
            'name': self.task_name,
            'user_ids': self.user_ids.ids,
            'date_deadline': self.date_deadline
        })

