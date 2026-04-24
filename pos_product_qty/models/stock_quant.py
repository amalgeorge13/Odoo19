from odoo import api,fields,models

class StockQuant(models.Model):

    _inherit = ['stock.quant','pos.load.mixin']


    @api.model
    def _load_pos_data_fields(self, config_id):
        """
        Adds the 'qty_available' field to the list of fields loaded into the POS.
        """
        data = super()._load_pos_data_fields(config_id)
        data += ['location_id','product_id','inventory_quantity_auto_apply']
        print(data)
        return data
    