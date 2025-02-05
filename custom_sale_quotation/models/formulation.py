from odoo import models, fields, api

class FormulationTemplate(models.Model):
    _name = 'formulation.template'
    _description = 'Plantilla de Formulación'

    name = fields.Char(string="Nombre de la Formulación", required=True)
    customer_id = fields.Many2one('res.partner', string="Cliente")  # Agregamos este campo
    product_id = fields.Many2one('product.product', string="Producto", ondelete="set null")
    line_ids = fields.One2many('formulation.template.line', 'formulation_id', string="Ingredientes")
    bom_id = fields.Many2one('mrp.bom', string="Lista de Materiales (BoM)", readonly=True)
     # Relación con Pedidos de Venta (sale.order)
    sale_order_ids = fields.One2many('sale.order', 'formulacion_template_id', string="Pedidos de Venta")

    def generate_bom(self):
        """Genera una BoM basada en la formulación"""
        for record in self:
            if not record.bom_id:
                bom = self.env['mrp.bom'].create({
                    'product_tmpl_id': record.product_id.product_tmpl_id.id,
                    'type': 'normal',
                    'bom_line_ids': [(0, 0, {
                        'product_id': line.product_id.id,
                        'product_qty': line.quantity_per_capsule,
                    }) for line in record.line_ids]
                })
                record.bom_id = bom.id
            else:
                record.bom_id.bom_line_ids.unlink()
                for line in record.line_ids:
                    self.env['mrp.bom.line'].create({
                        'bom_id': record.bom_id.id,
                        'product_id': line.product_id.id,
                        'product_qty': line.quantity_per_capsule,
                    })

class FormulationTemplateLine(models.Model):
    _name = 'formulation.template.line'
    _description = 'Línea de Formulación'

    formulation_id = fields.Many2one('formulation.template', string="Formulación")
    product_id = fields.Many2one('product.product', string="Ingrediente")
    quantity_per_capsule = fields.Float(string="Cantidad por Cápsula (mg)")
    