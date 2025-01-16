# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, _, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.depends('order_line.date_planned')
    def _compute_date_planned(self):
        for order in self:
            dates_list = order.order_line.filtered(lambda x: not x.display_type and x.date_planned).mapped(
                'date_planned')
            if dates_list:
                order.date_planned = fields.Datetime.to_string(max(dates_list))
            else:
                order.date_planned = False

    # def button_confirm(self):
    #     res = super(PurchaseOrder, self).button_confirm()
    #     for picking in self.picking_ids:
    #         for move in picking.move_lines:
    #             if move.purchase_line_id:
    #                 move.date_planned = move.purchase_line_id.date_planned
    #     return res


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def write(self, vals):
        res = super(PurchaseOrderLine, self).write(vals)
        if 'date_planned' in vals:
            for line in self:
                picking = line.move_ids.picking_id
                if picking:
                    picking.write({'scheduled_date': vals['date_planned']})
        return res

