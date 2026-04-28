from odoo import api, fields, models,Command
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.onchange('tag_ids')
    def _onchange_tag_ids(self):
        """
        when selecting tags automatic select corresponding assignees
        """
        assignees=[]
        tags=[]
        if not assignees:
            self.user_ids = False
        for tag in self.tag_ids:
            tags.append(tag.name)
        users=self.env['res.users'].search([('active','=',True)])
        for user in users:
            if user.category_ids:
                for tag in user.category_ids:
                    if tag.name in tags:
                        assignees.append(user.id)
        self.user_ids = assignees

    @api.onchange('stage_id')
    def onchange_stage_id(self):
        """
        When change stage into progress create timesheet
        if time sheet working hours false raise validation error
        """
        if self.stage_id.name == "In_Progress":
            timesheet_lines=[]
            for user in self.user_ids:

                timesheet_lines.append(Command.create({
                        'date': fields.Date.today(),
                        'employee_id': user.partner_id.employee_ids.id,
                    }))
            self.timesheet_ids=timesheet_lines

        if self.stage_id.name == "Done":
            for line in self.timesheet_ids:
                if not line.unit_amount:
                    raise ValidationError("Timesheet has no hours")
