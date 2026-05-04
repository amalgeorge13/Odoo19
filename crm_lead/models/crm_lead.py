from odoo import api, fields, models
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = "crm.lead"

    activitys = []

    # activity_ids = fields.One2many('mail.activity', 'crm_lead_id', string="Activities")

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        """
        when set customer automatically set the sales person based on region
        """
        if self.partner_id.state_id and self.partner_id.city and self.user_id.state_id and self.user_id.city:
            customer_state=self.partner_id.state_id
            customer_city = self.partner_id.city
            users=self.env['res.users'].search([('state_id','=',customer_state),('city','=',customer_city)])
            self.user_id=users[0].id

    @api.onchange("stage_id")
    def _onchange_stage_id(self):
        """
        when change state in to qualified then schedule 2 activities
        and restrict stage won without completing activities
        """
        if not self.ids and self.stage_id.name != 'New':
            raise ValidationError('Go After save')
        if self.stage_id.name == 'Qualified' and not self.activity_ids:
            activities=[2,4]
            for activity in activities:
                acti=self.env['mail.activity'].create({
                    'activity_type_id': activity,
                    'summary':'Activity',
                    'res_model_id':self.env['ir.model']._get_id('crm.lead'),
                    'res_model':'crm.lead',
                    'res_id':self.ids[0],
                    'user_id': self.user_id.id,
                })
                self.activitys.append(acti.id)
        if self.stage_id.name == 'Proposition':
            done_activities = self.env['mail.activity'].search_read([('active', '=', False),('id', 'in', self.activitys)], fields=('active', 'state'))
            if not done_activities:
                raise ValidationError('Go After Completing Atleast One Activity')

        if self.stage_id.name =='Won':
            for activity in self.activity_ids:
                if activity:
                    raise ValidationError('Go After Completing All Activity')

