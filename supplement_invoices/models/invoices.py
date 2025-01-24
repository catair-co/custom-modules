
from odoo import models, fields

class SupplementQuotation(models.Model):
    _inherit = 'supplement.quotation'

    advance_payment = fields.Boolean(string="Anticipo Pagado", default=False)

    def create_advance_invoice(self):
        for record in self:
            advance_amount = record.capsule_qty * 0.5  # Ejemplo de cálculo
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': record.customer_id.id,
                'invoice_line_ids': [(0, 0, {'name': 'Anticipo', 'price_unit': advance_amount})],
            })
