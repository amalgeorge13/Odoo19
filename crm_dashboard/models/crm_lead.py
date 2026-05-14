from odoo import models, api, fields
from dateutil.relativedelta import relativedelta


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_tiles_data(self,new):
        """Fetch whole lead data for creating Dashboard"""
        company_id = self.env.company
        domain=[('company_id', '=', company_id.id),('user_id', '=', self.env.user.id)]
        act_domain = [('res_model_id', '=', self.env['ir.model']._get_id('crm.lead'),)]
        lost_lead_domain = [('won_status', '=', 'lost'), ('user_id', '=', self.env.user.id), ('active', '=', False),
                            ('type', '=', 'opportunity')]
        today = fields.Datetime.today()
        if new:
            if new=='year':
                check_date=today - relativedelta(years=1)
            if new=='quarter':
                check_date=today - relativedelta(months=4)
            if new=='month':
                check_date=today - relativedelta(months=1)
            if new=='week':
                check_date=today- relativedelta(weeks=1)
            domain = [('company_id', '=', company_id.id), ('user_id', '=', self.env.user.id),
                      ('create_date', '>=', check_date)]
            act_domain = [('res_model_id', '=', self.env['ir.model']._get_id('crm.lead')),
                          ('create_date', '>=', check_date)]
            lost_lead_domain = [('won_status', '=', 'lost'), ('user_id', '=', self.env.user.id),
                                ('active', '=', False), ('type', '=', 'opportunity'),
                                ('create_date', '>=', check_date)]
        leads = self.search(domain)


        my_leads = leads.filtered(lambda r: r.type == 'lead')
        my_opportunity = leads.filtered(lambda r: r.type == 'opportunity')
        currency = company_id.currency_id.symbol
        expected_revenue = sum(my_opportunity.mapped('expected_revenue'))

        revenue = self.env['sale.order'].search(
            [('user_id', '=', self.env.user.id), ('opportunity_id', 'in', my_opportunity.ids)]).mapped('amount_total')
        win_leads = leads.filtered(lambda r: r.stage_id.name == 'Won')

        lost_leads = self.search(lost_lead_domain)

        ratio = len(win_leads) * (100 / (len(win_leads) + len(lost_leads)))

        activities = self.env['mail.activity'].search(act_domain)
        call = 0
        email = 0
        meeting = 0
        document = 0
        todo=0
        for activity in activities:
            if activity.activity_type_id.name == 'Call':
                call = call + 1
            if activity.activity_type_id.name == 'Email':
                email = email + 1
            if activity.activity_type_id.name == 'Meeting':
                meeting = meeting + 1
            if activity.activity_type_id.name == 'To-Do':
                todo = todo + 1
            if activity.activity_type_id.name == 'Document':
                document = document + 1


        table_data=[0,0,0,0,0,0,0,0,0,0,0,0]
        for lead in my_leads:
            table_data[lead.create_date.month-1]=table_data[lead.create_date.month-1]+1

        banner = 0
        e_mail = 0
        google = 0
        website = 0
        linkedin = 0
        for lead in my_leads:
            if lead.medium_id.name == 'Banner':
                banner = banner + 1
            if lead.medium_id.name == 'Email':
                e_mail = e_mail + 1
            if lead.medium_id.name == 'Google Adwords':
                google = google + 1
            if lead.medium_id.name == 'Website':
                website = website + 1
            if lead.medium_id.name == 'LinkedIn':
                linkedin = linkedin + 1

        services = 0
        products = 0
        sale = 0
        christmas = 0
        for lead in my_leads:
            if lead.campaign_id.name == 'Email Campaign - Services':
                services = services + 1
            if lead.campaign_id.name == 'Email Campaign - Products':
                products = products + 1
            if lead.campaign_id.name == 'Sale':
                sale = sale + 1
            if lead.campaign_id.name == 'Christmas Special':
                christmas = christmas + 1

        return {
            'total_leads': my_leads.ids,
            'total_opportunity': my_opportunity.ids,
            'expected_revenue': expected_revenue,
            'revenue': sum(revenue),
            'currency': currency,
            'win_leads': len(win_leads),
            'lost_leads': len(lost_leads),
            'ratio': round(ratio, 1),
            'activities': [call, email, meeting, todo, document],
            'table_data': table_data,
            'medium': [e_mail, google, banner, website, linkedin],
            'campaign':[services, products, sale, christmas],
        }