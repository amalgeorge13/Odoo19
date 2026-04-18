from odoo import fields, models, api

class FleetServiceOrderChecklist(models.Model):
    _name = 'fleet.service.order.checklist'

    order_id = fields.Many2one('fleet.service.order')
    task_name = fields.Char(string='Task Name')
    is_done = fields.Boolean(string='Is Done')
    note = fields.Text(string='Note')
    check_list_count=fields.Integer(string='Check List Count',compute='_compute_count')
    check_list_completed=fields.Integer(string='Check List Completed',compute='_compute_count')
    percentage = fields.Float(string='Percentage',compute='_compute_percentage')

