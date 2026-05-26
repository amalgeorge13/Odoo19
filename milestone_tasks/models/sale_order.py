from odoo import api, fields, models
from odoo import Command


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def create_project(self):
        milestones = []
        self.env['project.project'].create({
            'name': self.name,
        })
        project_id = self.env['project.project'].search([('name', '=', self.name)], limit=1,order='id desc')
        for line in self.order_line:
            if line.milestone not in milestones:
                self.env['project.task'].create({
                    'name': 'Milestone' + str(line.milestone),
                    'project_id': project_id.id,
                    'description': 'Task',
                    'user_ids': self.user_id,
                    'sale_order_id': self.id,
                })
                milestones.append(line.milestone)

            task_name = 'Milestone' + str(line.milestone)
            parent_id = self.env['project.task'].search([('name', '=', task_name)], limit=1)
            self.env['project.task'].create({
                'name': 'Milestone' + str(line.milestone) + '-' + line.product_id.name,
                'parent_id': parent_id.id
            })

