from odoo import fields, models, api, Command
from odoo.exceptions import UserError

class ProductRequest(models.Model):
    _name = "product.request"
    _description = "Product Request"

    name = fields.Char(string='Name', required=True, default='New', readonly=True)
    vendor_id = fields.Many2one('res.partner', required=True,copy=False)
    employee_id = fields.Many2one('res.users', required=True,copy=False,
                                  default=lambda self: self.env.user.id)
    order_date = fields.Datetime(string='Order Date',default=fields.Date.today())
    product_line_ids = fields.One2many(comodel_name='product.line',inverse_name='request_id')
    state = fields.Selection([('draft','Draft'),('submit','Submit'),('approve','approved'),
                              ('confirm','Confirmed'),('reject','Reject')],default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        """sequence creation"""
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = (self.env['ir.sequence'].next_by_code('product.request'))
        if not self.env.user.has_group('component_request.group_requistion_user'):
            raise UserError('Only Requistion User can Approve Components Request.')
        return super().create(vals_list)
    def action_submit(self):
        print(self.state)
        self.state = 'submit'

    def action_approve(self):
        """When Approving Check user group"""
        if self.env.user.has_group('component_request.group_requistion_manager'):
            self.state = 'approve'
        else:
            raise UserError('Only Requistion Manager can Approve Components Request.')

    def action_reject(self):
        """When Rejecting Check user group"""
        if self.env.user.has_group('component_request.group_requistion_head'):
            self.state = 'reject'
        else:
            raise UserError('Only Requistion Head can Reject Components Request.')

    def action_confirm(self):
        """Checking user group and create purchase order and internal transfer order"""
        vendor=[]
        non_seller_order_line=[]
        move_line=[]
        if self.env.user.has_group('component_request.group_requistion_head'):
            self.state = 'confirm'
            for line in self.product_line_ids:
                if line.operation_type_id.name == 'Receipts' and line.product_id.seller_ids:
                    minimum = min(line.product_id.seller_ids, key=lambda l: l.price)
                    print(minimum.partner_id, minimum.price)
                    if minimum.partner_id not in vendor:
                        seller_order_line = [
                            Command.create({
                                'product_id': line.product_id.id,
                                'product_qty': line.quantity,
                                'price_unit': minimum.price,
                            })]
                        vendor.append(minimum.partner_id)
                        self.env['purchase.order'].create({
                            'partner_id': minimum.partner_id.id,
                            'state': 'draft',
                            'order_line': seller_order_line,
                        })
                    else:
                        PO = self.env['purchase.order'].search(
                            [('state', '=', 'draft'), ('partner_id', '=', minimum.partner_id)],
                            limit=1, order='name desc')

                        if line.product_id in PO.product_id:
                            for po_line in PO.order_line:
                                if po_line.product_id == line.product_id:
                                    po_line.product_qty = po_line.product_qty + line.product_qty


                        else:
                            self.env['purchase.order.line'].create({
                                'order_id': PO.id,
                                'product_id': line.product_id.id,
                                'product_qty': line.quantity,
                                'price_unit': minimum.price,

                            })
                if line.operation_type_id.name == 'Receipts' and not line.product_id.seller_ids:
                    non_seller_order_line.append(Command.create({
                        'product_id': line.product_id.id,
                        'product_qty': line.quantity,
                    }))

                    if non_seller_order_line:
                        self.env['purchase.order'].create({
                            'partner_id': self.vendor_id.id,
                            'state': 'draft',
                            'order_line': non_seller_order_line
                        })
                if line.operation_type_id.name == 'Internal Transfers':

                    move_line.append(Command.create({
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.quantity,
                    }))

                    self.env['stock.picking'].create({
                        'partner_id': self.vendor_id.id,
                        'move_ids': move_line,
                        'location_id':5,
                        'picking_type_id':line.operation_type_id.id
                    })


        else:
            raise UserError('Only Requistion Head can Confirm Components Request.')


