from odoo import fields,models,api

class labor_cost(models.Model):
    _name = 'labor.cost'
    _description = 'labor.cost'
    _rec_name = "reference"

    reference = fields.Many2one('vehicle.repair', string="reff")
    labor_name = fields.Many2one('hr.employee', string="Labor Name")
    hourly_cost = fields.Float(string="Hourly Cost")
    hours_spend = fields.Float(string="Hours Spend")
    labor_cost = fields.Float(string="Labor Cost", compute="_compute_labor_cost")

    @api.depends('hourly_cost','hours_spend')
    def _compute_labor_cost(self):
        for record in self:
            record.labor_cost = record.hourly_cost * record.hours_spend