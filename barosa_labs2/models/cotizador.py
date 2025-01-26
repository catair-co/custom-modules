from odoo import models, fields, api

class Cotizador(models.Model):
    _name = 'cotizador'
    _description = 'Cotizador'

    name = fields.Char(string="Nombre", required=True)
    formulation_template_id = fields.Many2one(
        'formulation.template', 
        string="Plantilla de Formulación",
        help="Selecciona una plantilla de formulación para cargar las líneas automáticamente"
    )
    number_of_bottles = fields.Integer(
        string="Número de Botes", 
        required=True, 
        default=1, 
        help="Número total de botes a fabricar"
    )
    capsules_per_bottle = fields.Integer(
        string="Cápsulas por Bote", 
        required=True, 
        default=30, 
        help="Número de cápsulas en cada bote"
    )
    line_ids = fields.One2many(
        comodel_name='cotizador.line',
        inverse_name='cotizador_id',
        string="Líneas de Cotización"
    )

    @api.onchange('formulation_template_id', 'number_of_bottles', 'capsules_per_bottle')
    def _onchange_formulation_template(self):
        """Carga las líneas de cotización y calcula las cantidades basadas en botes y cápsulas."""
        if self.formulation_template_id:
            # Limpia las líneas actuales
            self.line_ids = [(5, 0, 0)]
            
            # Calcula el total de cápsulas
            total_capsules = self.number_of_bottles * self.capsules_per_bottle
            
            # Agrega nuevas líneas basadas en la plantilla seleccionada
            self.line_ids = [
                (0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': line.quantity * total_capsules,
                    'price_unit': line.product_id.list_price,
                })
                for line in self.formulation_template_id.cotizacion_line_ids
            ]


class CotizadorLine(models.Model):
    _name = 'cotizador.line'
    _description = 'Línea del Cotizador'

    cotizador_id = fields.Many2one(
        comodel_name='cotizador',
        string="Cotizador",
        required=True,
        ondelete="cascade"
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Producto",
        required=True
    )
    quantity = fields.Float(string="Cantidad", required=True, default=1.0)
    price_unit = fields.Float(string="Precio Unitario", related="product_id.list_price", readonly=True)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit