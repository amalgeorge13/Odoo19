from odoo import fields, models,api
from ast import literal_eval


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _description = "Product Template"

    loc_qty = fields.Float(string="Quantity",compute="_compute_location_wise_qty")

    @api.model
    def _load_pos_data_fields(self, config_id):
        """
        Adds the 'qty_available' field to the list of fields loaded into the POS.
        """
        data = super()._load_pos_data_fields(config_id)
        data += ['loc_qty']
        print(data)
        return data

    def _compute_location_wise_qty(self):
        loc_id = self.env['ir.config_parameter'].sudo().get_param('testing_settings.location_id')
        loc_id = literal_eval(loc_id)
        for rec in self:
            qtyy = self.env['stock.quant'].search(
                [('location_id', '=',loc_id),('product_id','in',rec.product_variant_ids.ids)]).mapped('available_quantity')
            total_qty = 0
            for qty in qtyy:
                if qty>0:
                    total_qty = total_qty + qty
            rec.loc_qty = total_qty

