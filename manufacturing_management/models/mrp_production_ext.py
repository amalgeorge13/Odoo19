# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo import Command
from odoo.exceptions import ValidationError

class MrpProductionExt(models.Model):
    """Handling Mrp Production Ext Model"""
    _name = 'mrp.production.ext'
    _description = 'Mrp Production Ext'

    name =fields.Char(string='Name',required=True,default='New',copy=False,readonly=True)
    product_id = fields.Many2one(comodel_name='product.template', string='Product',)
    bom_id = fields.Many2one(comodel_name='mrp.bom', string='BOM')
    quantity = fields.Float(string='Quantity')
    planned_date = fields.Date(string='Planned Date')
    state = fields.Selection([('draft', 'Draft'),('confirmed','Confirmed'),('in_progress','In Progress'),
                              ('done','Done'),('cancelled','Cancelled')],string='Status',default='draft')
    material_line_ids=fields.One2many(comodel_name='mrp.production.material.line', inverse_name='production_id')
    available = fields.Boolean(string='Available',default=False)
    produced_qty = fields.Float(string='Produced Qty')

    @api.model_create_multi
    def create(self, vals_list):
        """sequence creation"""
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = (self.env['ir.sequence'].next_by_code('mrp.production.ext'))
        return super().create(vals_list)

    @api.onchange('bom_id','quantity',)
    def _onchange_bom_id(self):
        """material line creation for BOM when selecting BOM"""
        self.product_id = self.bom_id.product_tmpl_id.id
        self.material_line_ids = [Command.clear()]
        material_line = []
        for line in self.bom_id.bom_line_ids:
            material_line.append(Command.create({
                'product_id': line.product_id.id,
                'required_qty': line.product_qty * self.quantity,
                'available_qty': line.product_id.qty_available,
            })
            )
        self.material_line_ids = material_line

    def action_confirm(self):
        """Button for confirming Mrp Production Ext"""
        if self.bom_id and self.quantity>0:
            self.state = 'confirmed'
        else:
            raise ValidationError("select BOM and Quantity")

    def action_start_production(self):
        """button for start production"""
        for line in self.material_line_ids:
            if line.required_qty <= line.available_qty :
                self.state = 'in_progress'
                self.available = True
            else:
                raise ValidationError("Dont Have Enough Quantity")

    def action_consume_materials(self):
        """Button for consume materials"""
        for line in self.material_line_ids:
            line.consumed_qty = line.required_qty
            line.remaining_qty = line.available_qty - line.consumed_qty

    def fetch_materials(self):
        """Smart Button Fetch materials list"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Materials',
            'view_mode': 'list',
            'res_model': 'mrp.production.material.line',
            'domain': [('production_id', '=', self.name)],
            'context': {'create': False},
        }

    def action_done(self):
        """button for done production"""
        for line in self.material_line_ids:
            if line.consumed_qty:
                self.state = 'done'
            else:
                raise ValidationError("Manufacturing not done")

    def action_partial_production(self):
        """button for partial production"""
        produced=0
        for i in range(int(self.quantity)):
            for line in self.material_line_ids:
                if line.available_qty - (line.required_qty/self.quantity) >= 0:
                    line.available_qty = line.available_qty - (line.required_qty/self.quantity)
                    produced=produced+1
                else:
                    break
        self.produced_qty = produced/len(self.material_line_ids)
