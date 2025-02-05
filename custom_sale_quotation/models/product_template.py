from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_formulacion = fields.Boolean(string="Es una Formulación")
    is_envase = fields.Boolean(string="Es un Envase")
    is_tapa = fields.Boolean(string="Es una Tapa")
    is_etiqueta = fields.Boolean(string="Es una Etiqueta")

    compatible_envase_id = fields.Many2one('product.template', string="Compatible con Envase")