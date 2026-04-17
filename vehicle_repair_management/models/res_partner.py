from odoo import fields, models,api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    vehicle_ids = fields.One2many('vehicle.repair',string='Vehicle',inverse_name='customer_name')
    customer_state = fields.Selection([('non_service_customer','Non Service Customer'),
                                       ('service_customer','Service Customer')],default='non_service_customer')

    def action_get_vehicles_repair_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vehicles',
            'view_mode': 'list,form',
            'res_model': 'vehicle.repair',
            'domain': [('customer_name', '=', self.id)],
            'context': "{'create': False}"
        }

    def action_create_repair_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Repair',
            'view_mode': 'form',
            'res_model': 'vehicle.repair'
        }

    def action_archive(self):
        res = super().action_archive()
        repairs = self.env['vehicle.repair'].search([('active','=',True),('customer_name','=',self.id)])
        repairs.write({'active':False})
        return res

    def action_unarchive(self):
        res = super().action_unarchive()
        repairs = self.env['vehicle.repair'].search([('active','=',False),('customer_name','=',self.id)])
        repairs.write({'active':True})
        return res






