from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo import Command

class FleetServiceOrder(models.Model):
    _name = 'fleet.service.order'
    _description = 'Fleet Service Order'

    name = fields.Char(required=True,default='New')
    vehicle_id = fields.Many2one(comodel_name='fleet.vehicle',string='Vehicle')
    technician_id = fields.Many2one(comodel_name='hr.employee',string='Technician')
    service_date = fields.Date(string='Service Date')
    state = fields.Selection([('draft', 'Draft'),('confirmed', 'Confirmed'),('in_progress', 'In Progress'),
                              ('done','Done'),('cancelled','Cancelled')],string='State',default='draft')
    part_ids=fields.One2many('fleet.service.order.part','order_id',string='Parts')
    checklist_ids = fields.One2many('fleet.service.order.checklist','order_id',string='Checklists')
    parts_total = fields.Float(string='Total Parts',compute='_compute_total_parts')
    labour_cost = fields.Float(string='Labour Cost')
    grand_total = fields.Float(string='Grand Total',compute='_compute_grand_total')
    checklist_progress = fields.Float(string='Checklist Total',compute='_compute_checklist_progress')
    type_ids = fields.Many2many(comodel_name='checklist.type',string='Types')

    @api.model_create_multi
    def create(self, vals_list):
        """sequence creation"""
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = (self.env['ir.sequence'].next_by_code('fleet.service.order'))
        return super().create(vals_list)

    @api.depends('part_ids.amount')
    def _compute_total_parts(self):
        for record in self:
            all_parts_price = record.part_ids.mapped('amount')
            record.parts_total = sum(all_parts_price)

    @api.depends('parts_total','labour_cost')
    def _compute_grand_total(self):
        self.grand_total = self.labour_cost + self.parts_total
        print(len(self.checklist_ids))

    @api.depends('checklist_ids.is_done','checklist_ids')
    def _compute_checklist_progress(self):
        completed = 0
        for record in self.checklist_ids:
            if record.is_done:
                completed += 1
        if len(self.checklist_ids) or completed > 0:
            self.checklist_progress = completed / len(self.checklist_ids) * 100
        else:
            self.checklist_progress = 0
        if self.checklist_progress == 100:
            self.state = 'done'

    def action_confirm(self):
        if len(self.part_ids)>0:
            self.state = 'confirmed'
        else:
            raise ValidationError('No Parts Found')
    def action_start(self):
        if self.technician_id:
            self.state = 'in_progress'
        else:
            raise ValidationError('No Technician Found')

    def action_cancel(self):
        if self.state != 'done':
            self.state = 'cancelled'

    def action_generate_checklist(self):

        names = self.checklist_ids.mapped('task_name')
        checklist_lines = []

        for type in self.type_ids:
            if type.name in names:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Duplicates!',
                        'message': 'checklist already exists',
                        'type': 'warning',
                        'sticky': True
                    }
                }
            else:
                checklist_lines.append(Command.create({
                    'task_name': type.name,
                }))
        self.checklist_ids = checklist_lines
