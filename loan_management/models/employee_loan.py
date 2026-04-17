
from odoo import fields, models, api
from odoo.cli import Command
from odoo.exceptions import ValidationError
from odoo import Command


class EmployeeLoan(models.Model):
    _name = 'employee.loan'
    _description = 'Employee Loan'

    name = fields.Char(string='Name',required=True,default='New',readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  domain=[('loan_not_allowed','=',False)])
    loan_amount = fields.Float(string='Loan Amount')
    installment_count = fields.Integer(string='Installment Count',required=True)
    start_date = fields.Date(string='Start Date')
    state = fields.Selection([('draft', 'Draft'),('approved', 'Approved'),('ongoing', 'Ongoing'),
                              ('paid', 'Paid')],string='State',default='draft')
    loan_line_ids=fields.One2many('employee.loan.line','loan_id',string='Loan Lines')
    installment_amount = fields.Float(string='Installment Amount')
    total_payable = fields.Float(string='Total Payable',compute='_compute_total_payable')
    paid_amount = fields.Float(string='Paid Amount',default=0,compute='_compute_paid_amount')
    balance_amount = fields.Float(string='Balance Amount',compute='_compute_balance_amount')
    a=fields.Integer(default=0)

    @api.model_create_multi
    def create(self, vals_list):
        """sequence creation"""
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = (self.env['ir.sequence'].next_by_code('employee.loan'))
        return super().create(vals_list)

    @api.depends('loan_amount')
    def _compute_total_payable(self):
        self.total_payable = self.loan_amount

    @api.onchange('loan_amount','installment_count')
    def _onchange_loan_amount(self):
        if self.loan_amount==0 or self.installment_count==0:
            self.installment_amount=0
        else:
            self.installment_amount = self.loan_amount/self.installment_count

    def action_approve_loan(self):
        print("button clicked")
        if self.loan_amount>0:
            self.state = 'approved'
        else:
            raise ValidationError('Loan Amount cannot be zero')

    def fetch_installments(self):
        """get installments on smart tab"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Installments',
            'view_mode': 'list',
            'res_model': 'employee.loan.line',
            'domain': [('loan_id', '=', self.name)],
            'context': {'create': False},
        }
    def generate_installment_records(self):
        loan_lines=[]
        for i in range(self.installment_count):
            loan_lines.append(Command.create({
                'amount': self.installment_amount,
            })
            )
        self.loan_line_ids=loan_lines
        self.state = 'ongoing'

    def pay_installments(self):

        self.loan_line_ids[self.a].paid = True
        self.a=self.a+1
        if len(self.loan_line_ids) == self.a:
            self.state = 'paid'

    @api.depends('loan_line_ids.paid','loan_line_ids.amount')
    def _compute_paid_amount(self):
        self.paid_amount =0
        for line in self.loan_line_ids:
            if line.paid:
                self.paid_amount = self.paid_amount + line.amount

    @api.depends('loan_line_ids.paid', 'loan_line_ids.amount')
    def _compute_balance_amount(self):
        self.balance_amount = self.total_payable
        for line in self.loan_line_ids:
            if line.paid:
                self.balance_amount = self.balance_amount - line.amount