from odoo import api, fields, models
from odoo import Command

class ProjectTemplate(models.Model):
    _name = 'project.template'
    _description = 'Project Template'

    name = fields.Char(string='Name',required=True)
    user_id = fields.Many2one('res.users', string='Project Manager')
    partner_id = fields.Many2one('res.partner', string='Customer')
    tag_ids = fields.Many2many('project.tags', string='Tags')
    task_ids = fields.Many2many('task.template', string='Tasks')

    def create_project(self):
        """Creating Project"""
        tasks=[]
        if self.task_ids:
            for task in self.task_ids:
                tasks.append(Command.create({
                    'name': task.task_name,
                    'user_ids': task.user_ids.ids,
                    'date_deadline': task.date_deadline
                }))

        self.env['project.project'].create({
            'name' : self.name,
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'tag_ids': self.tag_ids.ids,
            'task_ids': tasks
        })
