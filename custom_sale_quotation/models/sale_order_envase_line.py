from odoo import models, fields

class SaleOrderEnvaseLine(models.Model):
    _name = 'sale.order.envase.line'
    _description = "Líneas dinámicas de selección de productos según envase"

    order_id = fields.Many2one('sale.order', string="Pedido Relacionado", ondelete='cascade')
    categoria_id = fields.Many2one('product.category', string="Categoría")
    name = fields.Char(string="Nombre de la Categoría")
    product_id = fields.Many2one(
        'product.product',
        string="Producto",
        domain="[('categ_id', '=', categoria_id)]"  # Solo permite seleccionar productos de esa categoría
    )