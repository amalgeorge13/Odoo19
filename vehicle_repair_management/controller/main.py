from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

class RepairRequest(http.Controller):
    @http.route('/repair_request', auth='public', website=True)
    def repair_request(self):
        """load data from database for dropdown values"""
        partners = request.env['res.partner'].sudo().search([])
        users = request.env['res.users'].sudo().search([])
        vehicle_types = request.env['fleet.vehicle.model.category'].sudo().search([])
        vehicle_models = request.env['fleet.vehicle.model'].sudo().search([])
        datas = {
            'partners': partners,
            'users': users,
            'vehicle_types': vehicle_types,
            'vehicle_models': vehicle_models,
        }
        return request.render('vehicle_repair_management.repair_request_form_template', datas)

    @http.route(['/repair_request_form'], type='http', auth="public", website=True)
    def repair_request_form(self, **post):
        """for submission ,create records in model"""
        partner = post.get('partners')
        email = post.get('email')
        user = post.get('users')
        if partner and email and user:
            print(partner,email,user)
            request.env['vehicle.repair'].sudo().create({
                'customer_name': partner,
                'email': email,
                'service_advisor': user,
                'vehicle_type': post.get('vehicle_types'),
                'vehicle_model': post.get('vehicle_models'),
                'vehicle_number': post.get('vehicle_number'),
            })
        else:
            raise ValidationError('Please provide Details')
        return request.render('vehicle_repair_management.customer_success_template')
