from odoo import fields, models, api

class Absentees(models.Model):
    _name = 'absentees.employee'
    _description = 'Absentees'

    employee_id = fields.Many2one('hr.employee',string="Employee")
    date = fields.Date(string="Date",default=fields.Date.today())

    def fetch_employee(self):
        """fetch employee details"""
        today = fields.Date.today()
        attendance = self.env["hr.attendance"].search([('check_in', '>=',today)])
        employees = self.env["hr.employee"].search([])
        attendees=[]
        for emp in attendance:
            attendees.append(emp.employee_id)

        for emp in employees:
            if emp not in attendees:
                self.env['absentees.employee'].create({
                    'employee_id':emp.id,
                    'date':today
                })
