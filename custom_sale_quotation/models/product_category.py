from odoo import models

class ProductCategory(models.Model):
    _inherit = 'product.category'

    def name_get(self):
        """ Mostrar solo el nombre de la categoría sin la jerarquía. """
        result = []
        for category in self:
            result.append((category.id, category.name))  # 🔥 Solo muestra el nombre
        return result