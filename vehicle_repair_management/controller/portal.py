from odoo import http
from odoo.http import request

class RepairOrders(http.Controller):
    @http.route('/my/repair_orders', auth='public', website=True)
    def repair_orders(self):
        """repair records of portal user"""
        repairs = request.env['vehicle.repair'].sudo().search_read(domain=[('customer_name','=',self.env.user.partner_id)],
            fields=['repair_reference', 'start_date', 'total_amount', 'id'], order='repair_reference desc')

        return request.render('vehicle_repair_management.portal_my_repair_orders', {
            'repairs': repairs,
        })
    @http.route('/repair_details/<int:id>', auth='public', website=True)
    def repair_details(self,id):
        """details of selected repair record"""
        print(id)

        repair_record=request.env['vehicle.repair'].sudo().browse(id)
        return request.render('vehicle_repair_management.portal_my_repair_details',{
            'repair_record': repair_record,
        })