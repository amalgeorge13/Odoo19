from odoo import api, fields, models

class EmployeeLoanLine(models.Model):
    _name = 'employee.loan.line'
    _description = 'Employee Loan Line'

    loan_id = fields.Many2one(comodel_name='employee.loan',string='Loan Line')
    date = fields.Date(string='Date')
    amount = fields.Float(string='Amount')
    paid = fields.Boolean(string='Paid')