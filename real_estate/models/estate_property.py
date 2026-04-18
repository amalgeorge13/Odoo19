from itertools import count

from odoo.exceptions import ValidationError
from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.orm.fields_relational import One2many


def get_date(self):
    today = fields.Date.today()
    date_after_3month = today + relativedelta(months=3)
    return date_after_3month

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _rec_name = 'property_name'
    _order = 'id desc'

    property_name = fields.Char(string="Property Name",required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date Availability",default=get_date,copy=False)
    expected_price = fields.Float(string="Expected Price",required=True)
    _check_expected_price = models.Constraint('CHECK(expected_price>0)','Expected price must be strictly positive value')
    selling_price = fields.Float(string="Selling Price",readonly=True,copy=False)
    bedrooms = fields.Integer(string="Bed rooms",default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(string="Garden Orientation",selection=[('north','North'),('south','South'),('east','East'), ('west','West')])
    active = fields.Boolean(string="Active",default=True)
    state =fields.Selection(string="Status",
                             selection=[('new','New'),('offer_received','Offer Received'), ('offer_accepted','Offer Accepted'), ('sold','Sold'),('cancelled','Cancelled')],
                             default='new',copy=False)
    property_type_name = fields.Many2one(comodel_name='property.types',string="Property Type")
    user_name = fields.Many2one(comodel_name='res.users',string="Salesman")
    partner_name = fields.Many2one(comodel_name='res.partner',string="Buyer")
    property_tag_name = fields.Many2many(comodel_name='property.tags',string="Property Tag")
    offer_ids= fields.One2many(comodel_name='property.offers',inverse_name="property_id")
    total_area = fields.Integer(string="Total Area",compute='_compute_total_area',readonly=True,store=True)
    best_offer= fields.Float(string="Best Offer",readonly=True,compute='_compute_best_offer',store=True)
    sequence = fields.Integer('Sequence', default=1)



    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            prices=record.offer_ids.mapped('price')
            record.best_offer = max(prices) if prices else 0

    @api.onchange("garden")
    def _onchange_garden(self):
            if self.garden:
                self.garden_area = 10
                self.garden_orientation = 'north'
            else:
                self.garden_area = 0
                self.garden_orientation = ''

    def action_sold(self):
            if self.state == 'cancelled':
                raise UserError(message="You can't. The property already canceled")
            else:
                self.state = 'sold'


    def action_cancel(self):
            if self.state == 'sold':
                raise UserError(message="You can't. The property already sold")
            else:
                self.state = 'cancelled'



    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price > 0:
                if record.selling_price < record.expected_price * .9:
                    raise ValidationError("selling price must be above 90% of the expected price")





class PropertyType(models.Model):
    _name = "property.types"
    _description = "Real Estate Property Types"
    _rec_name = 'property_type_name'
    _order = 'property_type_name'

    property_type_name = fields.Char(string="Property Type",required=True)
    _unique_type_name=models.Constraint('UNIQUE(property_type_name)','duplicates doesnt allowed')
    property_ids =fields.One2many(comodel_name='estate.property',inverse_name="property_type_name")
    offer_ids=fields.One2many(comodel_name='property.offers',inverse_name="property_id")
    offer_count=fields.Integer(string="Offers",compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.property_ids.mapped('offer_ids'))

    # def action_offers(self):
    #     print(list())

class PropertyTag(models.Model):
    _name = "property.tags"
    _description = "Real Estate Property Tags"
    _rec_name = 'property_tag_name'
    _order='property_tag_name'

    property_tag_name = fields.Char(string="Property Tag",required=True)
    color = fields.Integer()
    _unique_tag_name=models.Constraint('UNIQUE(property_tag_name)','duplicates doesnt allowed')