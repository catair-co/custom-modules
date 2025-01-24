
from odoo import models, fields

class SupplementQuotation(models.Model):
    _inherit = 'supplement.quotation'

    raw_material_cost = fields.Float(string="Costo Materias Primas", required=True)
    encapsulation_cost = fields.Float(string="Costo Encapsulado", compute="_compute_encapsulation_cost", store=True)

    def _compute_encapsulation_cost(self):
        for record in self:
            record.encapsulation_cost = (record.capsule_qty / 1000) * 10.0  # Ejemplo
