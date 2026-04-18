from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    person_commission_amount = fields.Float(string="Commission Amount of Person",compute="_compute_commission_amount",readonly=True)
    team_commission_amount = fields.Float(string="Commission Amount of Team",compute="_compute_commission_amount",readonly=True)




    # def fetch_amount(self):
    #     print(self.amount_total)
    #     print(self.user_id.commi_plan_id.name)
    #     print(self.team_id.commission_plan_id)
    #     if self.user_id.commi_plan_id.type == 'revenue_wise':
    #
    #         for new in self.user_id.commi_plan_id.revenue_wise_ids:
    #             if new.from_amount <= self.amount_total <= new.to_amount:
    #                 self.person_commission_amount= new.rate/100 * self.amount_total
    #
    #         for new in self.team_id.commission_plan_id.revenue_wise_ids:
    #             if new.from_amount <= self.amount_total <= new.to_amount:
    #                 self.team_commission_amount= new.rate/100 * self.amount_total

    def fetch_commission_amount_person(self):
        if self.user_id.commi_plan_id.mode =='straight':
            for new in self.user_id.commi_plan_id.revenue_wise_ids:
                if new.from_amount <= self.amount_total <= new.to_amount:
                    self.person_commission_amount = new.rate / 100 * self.amount_total
                    break
        elif self.user_id.commi_plan_id.mode == 'graduated':
            for new in self.user_id.commi_plan_id.revenue_wise_ids:
                if new.from_amount <= self.amount_total:
                    if new.to_amount <= self.amount_total:
                        self.person_commission_amount = self.person_commission_amount + new.rate / 100 * (new.to_amount - new.from_amount)

                    else:
                        balance = self.amount_total - new.from_amount
                        self.person_commission_amount = self.person_commission_amount +((new.rate / 100) * balance)
                        print(self.person_commission_amount)
                        break


    def fetch_commission_amount_team(self):
        if self.team_id.commission_plan_id.mode == 'straight':
            for new in self.team_id.commission_plan_id.revenue_wise_ids:
                if new.from_amount <= self.amount_total <= new.to_amount:
                    self.team_commission_amount= new.rate/100 * self.amount_total
                    break
        elif self.team_id.commission_plan_id.mode == 'graduated':
            for new in self.team_id.commission_plan_id.revenue_wise_ids:
                if new.from_amount <= self.amount_total:
                    if new.to_amount <= self.amount_total:
                        self.team_commission_amount = self.team_commission_amount + new.rate / 100 * (new.to_amount - new.from_amount)
                    else:
                        balance = self.amount_total - new.from_amount
                        self.team_commission_amount = self.team_commission_amount +((new.rate / 100) * balance)
                        break


    @api.depends('amount_total','user_id','user_id.commi_plan_id','user_id.commi_plan_id.type',
                 'team_id','team_id.commission_plan_id','team_id.commission_plan_id.type',)
    def _compute_commission_amount(self):
        self.person_commission_amount =0
        self.team_commission_amount = 0
        if self.user_id and self.user_id.commi_plan_id and self.user_id.commi_plan_id.type == 'revenue_wise':
                self.fetch_commission_amount_person()
        if self.team_id and self.team_id.commission_plan_id and self.team_id.commission_plan_id.type == 'revenue_wise':
            self.fetch_commission_amount_team()






