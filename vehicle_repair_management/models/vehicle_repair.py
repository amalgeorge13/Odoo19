# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo import Command

class VehicleRepair(models.Model):
    _name = "vehicle.repair"
    _description = "Vehicle Repair"
    _rec_name = 'repair_reference'
    _inherit = ('mail.thread')

    repair_reference = fields.Char("Reference", default='New',
                         copy=False, readonly=True, tracking=True, required=True)
    image = fields.Image()
    customer_name =fields.Many2one(comodel_name='res.partner',string="Customer",required=True,tracking=1)
    email = fields.Char(string="Email",related='customer_name.email',readonly=True)
    service_advisor = fields.Many2one('res.users', string="Service Advisor",required=True)
    vehicle_number = fields.Char( string="Vehicle Number",copy=False,required=True)
    _unique_vehicle_number = models.Constraint('UNIQUE(vehicle_number)',message="Unique Vehicle Number")
    mobile_number = fields.Char(related='customer_name.phone',string="Mobile Number")
    active = fields.Boolean(string="Active",default=True)
    start_date = fields.Date(string="Start Date",default=fields.Date.today)
    duration = fields.Integer(string="Duration",required=True,default=1)
    delivery_date = fields.Date(string="Delivery Date")
    service_type = fields.Selection([('free', 'Free'),('paid', 'Paid')])
    estimated_delivery_date = fields.Date(string="Estimated Delivery Date",compute="_compute_estimated_delivery_date")
    estimated_amount = fields.Float(string="Estimated Amount")
    state = fields.Selection([('draft', 'Draft'),('in_progress', 'In-Progress'),('ready_for_delivery','Ready For Delivery'),
                              ('done','Done'),('cancelled','Cancelled')],string="State",default='draft',tracking=1)
    customer_complaint=fields.Html(string="Customer Complaint")
    tags =fields.Many2many('repair.tags', string="Tags")
    vehicle_type = fields.Many2one('fleet.vehicle.model.category',string="Vehicle Type",required=True)
    vehicle_model = fields.Many2one('fleet.vehicle.model',string="Vehicle Model",domain="[('category_id','=',vehicle_type)]",required=True)
    company_id = fields.Many2one('res.company',string="Company",default= lambda self: self.env.company)
    parts_ids = fields.One2many('consumed.parts',string="Parts",inverse_name="reference")
    labor_ids = fields.One2many('labor.cost',string="Labor Cost",inverse_name="reference")
    parts_total_amount = fields.Float(string="Total Amount",compute="_compute_parts_total_amount")
    labor_total_amount = fields.Float(string="Total Amount",compute="_compute_labor_total_amount")
    payment_state=fields.Selection([('unpaid','Unpaid'),('paid','Paid')],default='unpaid',required=True,string="Payment Status",compute="_compute_payment_state")
    invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True)
    today=fields.Date.today()
    total_amount = fields.Float(string="Total Amount",compute="_compute_total_amount")




    @api.depends('parts_ids.amount')
    def _compute_parts_total_amount(self):
        for record in self:
            all_parts_price = record.parts_ids.mapped('amount')
            record.parts_total_amount = sum(all_parts_price)

    @api.depends('labor_ids.labor_cost')
    def _compute_labor_total_amount(self):
        for record in self:
            all_labor_price = record.labor_ids.mapped('labor_cost')
            record.labor_total_amount = sum(all_labor_price)

    @api.depends('parts_total_amount','labor_total_amount')
    def _compute_total_amount(self):
        self.total_amount = self.parts_total_amount + self.labor_total_amount

    @api.depends('start_date','duration')
    def _compute_estimated_delivery_date(self):
        for record in self:
            if record.start_date and record.duration:
                record.estimated_delivery_date = record.start_date+ relativedelta(days=record.duration)
            else:
                record.estimated_delivery_date = False



    def action_confirm(self):
        self.state = 'in_progress'
        self.customer_name.customer_state = 'service_customer'

    def action_ready_for_delivery(self):
        self.state = 'ready_for_delivery'
        template = self.env.ref('vehicle_repair_management.email_template_vehicle_delivery')
        template.send_mail(self.id, force_send=True)


    def action_done_repair(self):
        self.state = 'done'
        self.delivery_date = self.estimated_delivery_date

    def action_cancel(self):
        self.state = 'cancelled'

    @api.model_create_multi
    def create(self, vals_list):
        """sequence creation"""
        for vals in vals_list:
            if vals.get('repair_reference', 'New') == 'New':
                vals['repair_reference'] = (self.env['ir.sequence'].next_by_code('vehicle.repair'))
        return super().create(vals_list)



    @api.onchange('vehicle_type')
    def _onchange_vehicle_type(self):
        self.vehicle_model = False

    def repair_invoice(self):
        """invoice creation
        Once clicked, create a draft invoice adding the labor cost in hours and the amount, and also the consumed parts, quantity and price.
        If there is an unpaid invoice for the customer, add the invoice to the existing invoice."""

        invoice_lines = []

        draft_invoices = self.env['account.move'].search([
            ('state', '=', 'posted'),
            ('payment_state', '=', 'not_paid'),
            ('partner_id', '=', self.customer_name.id)])
        draft_invoices.write({'state':'cancel'})

        lines=draft_invoices.mapped('invoice_line_ids')

        for labor in self.labor_ids:
            invoice_lines.append(Command.create({
                'name': labor.labor_name.name,
                'product_id': 71,
                'quantity': labor.hours_spend,
                'price_unit': labor.hourly_cost,
            }))

        for part in self.parts_ids:
            invoice_lines.append(Command.create({
                'product_id': part.part_id.id,
                'name': part.part_id.name,
                'quantity': part.quantity,
                'price_unit': part.unit_price,
            }))

        for line in lines:
            invoice_lines.append(Command.create({
                'product_id':line.product_id.id,
                'name': line.product_id.name,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
            }))

        repair_invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.customer_name.id,
            'invoice_line_ids':invoice_lines
        })

        self.invoice_id = repair_invoice.id

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': repair_invoice.id
        }

    def action_get_invoices(self):
        """get invoices on smart tab"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'domain': [('id', '=', self.invoice_id.id)],
            'context': {'create': False},
            'res_id': self.invoice_id
        }

    @api.depends('invoice_id.payment_state')
    def _compute_payment_state(self):
        for record in self:
            if record.invoice_id.payment_state=='paid':
                record.payment_state = 'paid'
            else:
                record.payment_state = 'unpaid'

    def cron_archive(self):
        """cron job for Archive the records which are in cancelled state and been there for 1 month"""
        expired = fields.Date.today() - relativedelta(months=1)
        records = self.search([('state', '=', 'cancelled'),('active','=',True)])
        for record in records:
            if record.state == 'cancelled' and record.start_date < expired:
                record.active = False













