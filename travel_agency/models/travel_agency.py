
from odoo import fields, models, api
from odoo import Command

class TravelAgency(models.Model):
    _name = "travel.agency"
    _description = "Travel Agency"
    _rec_name = 'customer_name'


    customer_name= fields.Many2one( comodel_name='res.partner',string="Customer Name",required=True)
    today = fields.Date.today()
    age= fields.Integer(string="Age")
    no_of_people= fields.Integer(string="No of People")
    vehicle= fields.Many2one("vehicles",string="Vehicle")
    state=fields.Selection(string="State",selection=[('new','New'),('ongoing','Ongoing'),('booked','Booked'),('cancelled','Cancelled')],default='new')
    from_city= fields.Char(string="From City")
    to_city= fields.Char(string="To City")
    date= fields.Datetime(string="Date of Travel")
    no_of_days=fields.Integer(string="No of Days")
    driver_fare= fields.Float(string="Driver Fare")
    petrol_expense= fields.Float(string="Petrol Expense")
    room=fields.Boolean(string="Room")
    room_expense= fields.Float(string="Room Expense")
    food=fields.Boolean(string="Food")
    food_expense= fields.Float(string="Food Expense")
    total_expense= fields.Float(string="Total Expense",compute='_compute_total',store=True)
    @api.depends('driver_fare','petrol_expense','room_expense','food_expense')
    def _compute_total(self):
        for record in self:
            record.total_expense=record.driver_fare+record.petrol_expense+record.room_expense+record.food_expense

    @api.onchange("room")
    def _onchange_room(self):
        if not self.room:
            self.room_expense = 0


    @api.onchange("food")
    def _onchange_food(self):
        if  not self.food:
            self.food_expense = 0


    def action_booked(self):
            self.state = 'booked'


    def action_cancelled(self):
            self.state = 'cancelled'

    def action_reschedule(self):
            self.state = 'ongoing'


    def create_invoice(self):
        self.ensure_one()

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.customer_name.id,
            'invoice_date_due':self.date,
            'invoice_date': self.today,
            'invoice_line_ids': [
                Command.create({
                    'name': 'Driver Fare',
                    'quantity': 1,
                    'price_unit': self.driver_fare,
                }),Command.create({
                    'name': 'Petrol Expense',
                    'quantity': 1,
                    'price_unit': self.petrol_expense,
                }),Command.create({
                    'name': 'Room Expense',
                    'quantity': 1,
                    'price_unit': self.room_expense,
                }),Command.create({
                    'name': 'Food Expense',
                    'quantity': 1,
                    'price_unit': self.food_expense,
                })
            ]
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
        }




class Vehicles(models.Model):
    _name = "vehicles"
    _description = "Vehicles"
    _rec_name = 'vehicle_name'

    vehicle_name= fields.Char(string="Vehicle Name")
    no_of_seats= fields.Integer(string="No of Seats")
    vehicle_no= fields.Char(string="Vehicle Number")
    type= fields.Selection(string="Vehicle Type",selection=[("car","Car"),("van","Van"),("bus","Bus")])

