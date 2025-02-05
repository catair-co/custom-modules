from odoo import models, fields, api

class ConfirmProductCreationWizard(models.TransientModel):
    _name = 'confirm.product.creation.wizard'
    _description = "Confirmación de Creación de Producto"

    sale_order_id = fields.Many2one('sale.order', string="Pedido Relacionado")
    confirm = fields.Boolean(string="Confirmar Creación")

    def action_confirm(self):
        """ Confirma la creación del producto """
        if self.sale_order_id:
            self.sale_order_id.action_confirm_create_product()