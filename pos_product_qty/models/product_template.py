from odoo import fields, models,api


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _description = "Product Template"

    loc_id = fields.Many2one('stock.location')
    loc_qty = fields.Float(string="Quantity")

    @api.model
    def _load_pos_data_fields(self, config_id):
        """
        Adds the 'qty_available' field to the list of fields loaded into the POS.
        """
        data = super()._load_pos_data_fields(config_id)
        data += ['qty_available']
        print(data)
        return data

    # def fff(self):
    #     for rec in self:
    #         qtyy = self.env['stock.quant'].search(
    #             [('location_id', '=', rec.loc_id.id),('product_tmpl_id','=',rec.id)]).mapped('available_quantity')
    #         total_qty = 0
    #         for qty in qtyy:
    #             if qty>0:
    #                 total_qty = total_qty + qty
    #         rec.loc_qty = total_qty

    # @api.depends('loc_id')
    # def _compute_qty(self):
    #     for rec in self:
    #         a = self.env['stock.quant'].search_read([('location_id', '=', self.loc_id.id),('product_tmpl_id','=',self.id)],
    #                                                 fields=['location_id', 'display_name', 'product_tmpl_id',
    #                                                         'available_quantity'])
