from odoo import fields, models, api
from odoo import Command

class Packages(models.Model):
    _name = "packages"
    _description = "Packages"
    _rec_name = 'package_name'

    package_name= fields.Char(string="Package Name")
    from_city= fields.Char(string="From City")
    to_city= fields.Char(string="To City")
    no_days= fields.Integer(string="Days")
    price= fields.Float(string="Price")

class PackageBooking(models.Model):
    _name = "package.booking"
    _description = "Package Booking"
    _rec_name = 'booking_id'

    booking_id= fields.Char(string="Booking ID")
    _unique_booking_id=models.Constraint('UNIQUE(booking_id)','Duplicate Booking ID doesnt allowed')
    customer_name= fields.Many2one('res.partner',string="Customer",required=True)
    date=fields.Date(string="Date")
    package_name= fields.Many2one("packages",string="Package Name")
    no_of_people= fields.Integer(string="No of People")
    total_price= fields.Float(string="Price",compute='_compute_price',store=True)
    state= fields.Selection([('new','New'),('booked','Booked'),('cancelled','Cancelled')],string="State",default='new',required=True)
    today = fields.Date.today()


    @api.depends('package_name.price','no_of_people')
    def _compute_price(self):
        for record in self:
            record.total_price = record.no_of_people * record.package_name.price

    def package_invoice(self):
        self.ensure_one()

        package_invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.customer_name.id,
            'invoice_date': self.today,
            'invoice_line_ids': [
                Command.create({
                    'name': self.package_name.package_name,
                    'quantity': 1,
                    'price_unit': self.total_price,
                })
            ]
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': package_invoice.id,
        }

    def action_reschedule(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'booking.reschedule',
            'view_mode': 'form',
            'context': {
                'default_booking_id': self.id,
            }
        }
    def action_book(self):
        self.state = 'booked'

    def action_cancel(self):
        self.state = 'cancelled'

class BookingReschedule(models.Model):
    _name = "booking.reschedule"
    _description = "Booking Reschedule"
    _rec_name = 'booking_id'

    booking_id= fields.Many2one('package.booking',string="Booking ID")
    customer_name= fields.Many2one('res.partner',related='booking_id.customer_name',string="Customer")
    date_from= fields.Date(related='booking_id.date', string="From Date")
    date_to= fields.Date(string="To Date")

    def action_confirm_reschedule(self):
        old_booking = self.booking_id
        old_booking.state = 'cancelled'


        new_booking = self.env['package.booking'].create({
            'booking_id': 'R' + old_booking.booking_id,
            'customer_name': old_booking.customer_name.id,                        # Create new booking with modified booking_id
            'date': self.date_to,
            'package_name': old_booking.package_name.id,
            'no_of_people': old_booking.no_of_people,
            'state': 'new',
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'package.booking',
            'view_mode': 'form',
            'res_id': new_booking.id,
        }