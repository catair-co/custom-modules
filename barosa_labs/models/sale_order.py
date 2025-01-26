from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    formulation_template_id = fields.Many2one(
        comodel_name='formulation.template',
        string='Plantilla de Formulación',
        domain="[('customer_id', '=', False)]",  # Dominio inicial
        help='Selecciona una formulación pública o una vinculada al cliente de este pedido.'
    )
    num_bottles = fields.Integer(string='Número de Botes', default=1, required=True)
    capsules_per_bottle = fields.Integer(string='Cápsulas por Bote', default=60, required=True)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """
        Ajusta dinámicamente el dominio del campo formulation_template_id
        para mostrar solo plantillas públicas o asociadas al cliente seleccionado.
        """
        if self.partner_id:
            # Mostrar plantillas públicas y patentadas para el cliente seleccionado
            domain = [
                '|',
                ('customer_id', '=', False),  # Plantillas públicas
                ('customer_id', '=', self.partner_id.id),  # Patentadas para el cliente
            ]
        else:
            # Mostrar solo plantillas públicas si no hay cliente seleccionado
            domain = [('customer_id', '=', False)]
        return {'domain': {'formulation_template_id': domain}}

    @api.onchange('formulation_template_id', 'num_bottles', 'capsules_per_bottle')
    def _onchange_formulation_data(self):
        """
        Calcula las cantidades totales de ingredientes basadas en los datos de formulación
        y cantidad de botes.
        """
        if self.formulation_template_id and self.num_bottles > 0 and self.capsules_per_bottle > 0:
            total_capsules = self.num_bottles * self.capsules_per_bottle
            lines = []
            for line in self.formulation_template_id.line_ids:
                total_quantity = line.quantity_per_capsule * total_capsules
                lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': total_quantity,
                    'product_uom': line.product_id.uom_id.id,
                    'price_unit': line.product_id.lst_price,
                }))
            self.order_line = lines