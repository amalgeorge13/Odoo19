from odoo import models, api

class CrmLead(models.Model):
   _inherit = 'crm.lead'
   @api.model
   def get_tiles_data(self):
       company_id = self.env.company
       leads = self.search([('company_id', '=', company_id.id),
                            ('user_id', '=', self.env.user.id)])
       my_leads = leads.filtered(lambda r: r.type == 'lead')
       my_opportunity = leads.filtered(lambda r: r.type == 'opportunity')
       currency = company_id.currency_id.symbol
       expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
       print(expected_revenue)
       print(my_leads)
       print(my_opportunity)
       revenue = self.env['sale.order'].search([('user_id', '=', self.env.user.id),('opportunity_id','in',my_opportunity.ids)]).mapped('amount_total')
       win_leads = self.search([('stage_id', '=', 'Won'),('user_id', '=', self.env.user.id)])
       lost_leads = self.search([('won_status', '=','lost'),('user_id', '=', self.env.user.id),('active','=',False),('type','=','opportunity')])


       ratio =len(win_leads)*(100/(len(win_leads)+len(lost_leads)))
       print(ratio)
       print(len(win_leads))
       print(len(lost_leads))


       return {
           'total_leads': my_leads.ids,
           'total_opportunity': my_opportunity.ids,
           'expected_revenue': expected_revenue,
           'revenue': sum(revenue),
           'currency': currency,
           'win_leads': len(win_leads),
           'lost_leads': len(lost_leads),
           'ratio': round(ratio, 1),
       }

   def action_restore(self):
       print(self.won_status)