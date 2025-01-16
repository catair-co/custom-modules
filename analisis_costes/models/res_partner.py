from odoo import _, api, fields, models
from datetime import date
import calendar

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Para buscar proveedor dependiendo de los precios de compra
    def search(self, args, offset=None, limit=None, order=None, count=None):
        context = dict(self._context or {})
        args = args or []
        domain=[]
        if context.get('an_line_search_product'):
            supplier_info_ids = self.env['product.supplierinfo'].search([('product_tmpl_id', '=' ,context.get('an_line_search_product'))])
            partner_ids = supplier_info_ids.mapped('name').ids
            domain = [('id','in',partner_ids)]
        return super(ResPartner,self).search(domain + args, offset, limit, order, count)


    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        context = dict(self._context or {})
        args = args or []
        domain=[]
        if context.get('an_line_search_product'):
            supplier_info_ids = self.env['product.supplierinfo'].search([('product_tmpl_id', '=' ,context.get('an_line_search_product'))])
            partner_ids = supplier_info_ids.mapped('name').ids
            domain = [('id','in',partner_ids)]
            return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
        return super(ResPartner, self)._name_search(name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
        