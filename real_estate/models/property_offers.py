from datetime import timedelta
from odoo import fields, models, api
from odoo.exceptions import UserError


class PropertyOffers(models.Model):
    _name = "property.offers"
    _description = "Real Estate Property Offers"
    _rec_name = 'property_id'
    _order ='price desc'

    property_id = fields.Many2one(comodel_name='estate.property',string="Property",required=True)
    partner_name = fields.Many2one(comodel_name='res.partner',string="Partner",required=True)
    price = fields.Float(string="Price")
    _check_price = models.Constraint('CHECK(price > 0)','offer price must be strictly positive')
    validity = fields.Integer(string="Validity")
    deadline = fields.Date(string="Deadline",compute="_compute_deadline",inverse="_inverse_deadline",store=True)
    status =fields.Selection(string="Status",selection=[('accepted','Accepted'),('refused','Refused')],copy=False)

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            today = fields.Date.today()
            record.deadline = timedelta(days=record.validity)+ today

    def _inverse_deadline(self):
        for record in self:
            today = fields.Date.today()
            diff = record.deadline - today
            record.validity=diff.days

    def action_accepted(self):
        record: PropertyOffers
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == 'accepted' :
                    raise UserError("You cannot accept multiple offers for this property.")

            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.partner_name =record.partner_name

    def action_refused(self):
        self.status = 'refused'
        if self.property_id.selling_price == self.price:
            self.property_id.selling_price = 0
            self.property_id.partner_name = ""
