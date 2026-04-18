from odoo import api, fields, models
from odoo import Command
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    proj_id = fields.Many2one('project.project', string="Project",domain="[('partner_id','=',partner_id)]")
    task_count = fields.Integer(related="proj_id.task_count")
    total_tasks = fields.Integer(default=0)
    priority = fields.Integer(default=4)


    @api.onchange('partner_id')
    def onchange_partner_id(self):
        self.proj_id=False

    def action_view_tasks(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tasks',
            'view_mode': 'list,form',
            'res_model': 'project.task',
            'domain': [('sale_order_id', '=', self.id)],
            'context': {'create': False},
        }

    def find_priority(self,qty,qty_list):
        print(self.priority)
        if qty not in qty_list:
            qty_list.append(qty)
            self.priority=self.priority-1
            if self.priority < 0:
                self.priority = 0
                return str(self.priority)
            return str(self.priority)
        elif qty in qty_list:
            return str(self.priority)


    def create_task(self):
        if self.proj_id and self.task_count>0:
            raise ValidationError("Already have tasks related to this project")


        sub_tasks = []

        name = "SO/" + self.name + "-" + self.partner_id.name
        # print(self.order_line.search_read([]))
        sorted_order_lines = sorted(self.order_line, key=lambda l: l.product_uom_qty, reverse=True)

        print (sorted_order_lines)
        qty_list = []


        for line in sorted_order_lines:

            sub_tasks.append(Command.create({
                'name': line.product_id.name + "-" + str(line.product_uom_qty),
                'priority': self.find_priority(line.product_uom_qty,qty_list),
            }))
        self.env['project.task'].create({
            'name': name,
            'description': 'Task',
            'project_id': self.proj_id.id,
            'user_ids': self.user_id,
            'child_ids': sub_tasks,
            'sale_order_id':self.id
        })
        tasks = self.env['project.task'].search([('sale_order_id', '=', self.ids)])
        self.total_tasks = len(tasks)
        self.priority=4
        #
        #
        #
        # # print(self.proj_id.task_ids)
        # # for i in self.proj_id.task_ids:
        # #     print(i.child_ids)
        # #     for j in i.child_ids:
        # #         print(111111111,j.name)