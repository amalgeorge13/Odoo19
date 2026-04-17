# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, route


class WebsiteRepair(http.Controller):
   @http.route('/get_repair_records', auth="public", type='jsonrpc',
               website=True)
   def get_repair_records(self):
       """Get the website repairs for the snippet."""
       repairs = request.env['vehicle.repair'].sudo().search_read(
           fields=['repair_reference', 'image', 'customer_name', 'id'],limit=10,order='repair_reference desc')

       values = {
           'repairs': repairs,
       }
       return values

   @http.route('/fetch_details/<int:id>', type='http', auth="public", website=True)
   def fetch_details(self, id ):
       """fetch single repair details"""
       repair = request.env['vehicle.repair'].sudo().search_read([('id', '=', id)],
                fields=['repair_reference', 'image', 'customer_name','id', 'service_advisor', 'vehicle_number'])
       values = {
           'repair': repair[0],
       }
       return request.render('vehicle_repair_management.repair_details_template', values)
