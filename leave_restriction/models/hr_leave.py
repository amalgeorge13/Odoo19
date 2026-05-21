from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrLeave(models.Model):
    _inherit = "hr.leave"

    leave_members=[]

    def action_approve(self):
        """overriding action_approve button with restriction features"""
        leave_date=self.request_date_from
        department=self.department_id
        leave_members=self.search([('request_date_from','=',leave_date),('department_id','=',department),
                                   ('state','=','validate')])
        leave_members_count=len(leave_members)
        dep_members=self.env['hr.employee'].search([('department_id','=',department)])
        count_dep_members=len(dep_members)

        for leave_member in leave_members:
            self.leave_members.append(leave_member.employee_id.name)
        str_leave_members=("\n".join(self.leave_members))

        percentage=leave_members_count/count_dep_members * 100
        if percentage>50:
            raise ValidationError(f'already leave approved these employees:\n{str_leave_members}')
        return super().action_approve()
