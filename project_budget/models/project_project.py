from odoo import api, fields, models

class ProjectProject(models.Model):
    _inherit = 'project.project'

    budget = fields.Monetary(string="Budget")
    budget_spend = fields.Float('Budget Spend',compute='_compute_budget_spend')

    @api.depends('task_ids.timesheet_ids.unit_amount',
                 'task_ids.timesheet_ids.employee_id')
    def _compute_budget_spend(self):
        budget=0
        tasks=self.task_ids
        print('adfasdfasdf')
        for task in tasks:
            for timesheet in task.timesheet_ids:
                budget= budget + (timesheet.employee_id.hourly_cost * timesheet.unit_amount)
        if self.budget:
            self.budget_spend = (budget/self.budget) *100
            if self.budget_spend > 80:
                print(self.budget_spend)
                self.message_post(body='Budget spend is greater than 80 percent of budget')

                template = self.env.ref('project_budget.email_budget')
                template.send_mail(self.id, force_send=True)
        else:
            self.budget_spend = 0
