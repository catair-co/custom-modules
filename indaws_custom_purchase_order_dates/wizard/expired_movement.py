from odoo import fields, models, api, Command

class ExpiredMovement(models.TransientModel):
    _name = 'expired.movement'
    _description = 'Expired movement wizard'

    stock_quant_ids = fields.Many2many(string="Stock", comodel_name="stock.quant")
    new_location = fields.Many2one(string="New Location", comodel_name="stock.location", default=lambda self: self.get_default_location())

    def get_default_location(self):
        if self.env['stock.location'].search([('name', '=', 'My Company: Scrap')]):
            return self.env['stock.location'].search([('name', '=', 'My Company: Scrap')]).id
        else:
            return False

    @api.model
    def default_get(self, fields):
        record_ids = self._context.get('active_ids')
        result = super(ExpiredMovement, self).default_get(fields)
        if record_ids:
            if 'stock_quant_ids' in fields:
                result['stock_quant_ids'] = [(6, 0, self.env['stock.quant'].browse(record_ids).ids)]
        return result

    def action_change_expired_elements(self):
        for quant in self.stock_quant_ids:
            operation_type = self.env['stock.picking.type'].search([('name', '=', 'Transferencias internas')])
            movement = self.env['stock.picking'].create({
                'picking_type_id': operation_type.id,
                'location_id': quant.location_id.id,
                'location_dest_id': self.new_location.id,
                'move_line_ids_without_package': [Command.create({
                    'product_id': quant.product_id.id,
                    'product_uom_id': quant.product_id.uom_id.id,
                    'lot_id': quant.lot_id.id,
                    'location_id': quant.location_id.id,
                    'location_dest_id': self.new_location.id,
                    'qty_done': abs(quant.inventory_quantity_auto_apply),
                })]
            })
            movement.button_scrap()
            movement.action_confirm()
            movement.button_validate()
            if movement.state == 'done':
                quant.write({
                    'location_id': self.new_location.id
                })
        return {
            'name': 'Quant',
            'view_mode': 'tree',
            'res_model': 'stock.quant',
            'domain': [('id', 'in', self.stock_quant_ids.ids)],
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        # return {
        #     'type': 'ir.actions.act_window_close',
        # }
