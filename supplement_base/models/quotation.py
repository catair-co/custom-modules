
from odoo import models, fields

class SupplementQuotation(models.Model):
    _name = 'supplement.quotation'
    _description = 'Cotización de Suplementos Alimenticios'

    name = fields.Char(string="Referencia", required=True, default="Nueva Cotización")
    customer_id = fields.Many2one('res.partner', string="Cliente", required=True)
    capsule_qty = fields.Integer(string="Cantidad de Cápsulas", required=True)
