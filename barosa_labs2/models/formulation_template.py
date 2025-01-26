from odoo import models, fields

class FormulationTemplate(models.Model):
    _name = 'formulation.template'
    _description = 'Plantilla de Formulación'

    name = fields.Char(string='Nombre', required=True)
    
    # Líneas de ingredientes
    line_ids = fields.One2many(
        comodel_name='formulation.template.line',
        inverse_name='template_id',
        string='Líneas de Ingredientes'
    )
    
    # Patente de cliente (opcional)
    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Patente de Cliente',
        help='Cliente asociado a la patente de esta formulación. Si está vacío, será pública.'
    )
    
    # Pedidos relacionados
    sale_order_ids = fields.One2many(
        comodel_name='sale.order',
        inverse_name='formulation_template_id',
        string='Pedidos Relacionados',
        readonly=True
    )

    cotizacion_line_ids = fields.One2many(
        comodel_name='formulation.template.line', 
        inverse_name='template_id', 
        string='Líneas de Cotización'
    )

class FormulationTemplateLine(models.Model):
    _name = 'formulation.template.line'
    _description = 'Línea de Plantilla de Formulación'

    formulation_template_id = fields.Many2one(
        comodel_name='formulation.template',
        string="Plantilla de Formulación",
        required=True,
        ondelete="cascade"
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Producto",
        required=True
    )
    quantity_per_capsule = fields.Float(
        string="Cantidad por Cápsula",
        required=True,
        help="Cantidad del ingrediente por cápsula"
    )