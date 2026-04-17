
from odoo import models, api

class VehicleRepairReport(models.AbstractModel):
    _name = 'report.vehicle_repair_management.vehicle_repair_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):

        docs = data.get('form')
        customer = data.get('customer')
        advisor = data.get('advisor')
        return {
            'doc_ids': docids,
            'doc_model': 'vehicle.repair',
            'docs': docs,
            'customer': customer,
            'advisor':advisor
        }