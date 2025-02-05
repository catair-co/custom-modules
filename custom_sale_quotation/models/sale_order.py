from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    formulacion_template_id = fields.Many2one(
        'formulation.template',
        string="Plantilla de Formulación",
        ondelete='set null'  # ✅ Mejor usar 'set null' para evitar errores
    )

    num_capsulas_por_bote = fields.Integer(string="Número de Cápsulas por Bote", default=60)
    num_botes = fields.Integer(string="Número de Botes", default=1)

    total_capsulas = fields.Integer(
        string="Número Total de Cápsulas",
        compute="_compute_total_capsulas",
        store=True
    )

    @api.depends('num_capsulas_por_bote', 'num_botes')
    def _compute_total_capsulas(self):
        for order in self:
            order.total_capsulas = order.num_capsulas_por_bote * order.num_botes

    ingredientes_ids = fields.One2many(
        'sale.order.ingredientes', 
        'order_id', 
        string="Ingredientes de la Formulación"
    )

    nombre_nueva_formulacion = fields.Char(
        string="Nombre de Nueva Formulación",
        help="Si se modifican ingredientes, este nombre se usará para guardar la nueva formulación."
    )

    @api.onchange('formulacion_template_id', 'num_capsulas_por_bote', 'num_botes')
    def _onchange_formulacion_template_id(self):
        """ Modifica las cantidades de los ingredientes y detecta cambios en la lista. """
        if not self.formulacion_template_id:
            self.ingredientes_ids = [(5, 0, 0)]  # Borra ingredientes si no hay plantilla
            return

        ingredientes_actuales = {line.product_id.id: line for line in self.ingredientes_ids}
        nuevos_ingredientes = []

        for line in self.formulacion_template_id.line_ids:
            cantidad_total = line.quantity_per_capsule * self.num_capsulas_por_bote * self.num_botes

            if line.product_id.id in ingredientes_actuales:
                # Actualiza cantidades existentes
                ingredientes_actuales[line.product_id.id].quantity = cantidad_total
                ingredientes_actuales[line.product_id.id].subtotal = cantidad_total * line.product_id.list_price

                nuevos_ingredientes.append((1, ingredientes_actuales[line.product_id.id].id, {
                    'quantity': cantidad_total,
                    'subtotal': cantidad_total * line.product_id.list_price
                }))
            else:
                # Agregar nuevo ingrediente
                nuevos_ingredientes.append((0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': cantidad_total,
                    'price_unit': line.product_id.list_price,
                    'subtotal': cantidad_total * line.product_id.list_price
                }))

        # Si hay cambios en los ingredientes, solicita un nuevo nombre
        if set(ingredientes_actuales.keys()) != {line.product_id.id for line in self.formulacion_template_id.line_ids}:
            self.nombre_nueva_formulacion = ""

        self.ingredientes_ids = nuevos_ingredientes

    def action_confirm_create_product(self):
        """Verifica si la formulación se está eliminando antes de asignarla"""
        for order in self:
            if not order.nombre_nueva_formulacion:
                raise UserError("Debe ingresar un nombre para la nueva formulación.")

            _logger.info(f"Inicio - Pedido: {order.name}")

            try:
                # 🔹 Crea el producto final
                nuevo_producto = self.env['product.template'].create({
                    'name': order.nombre_nueva_formulacion,
                    'type': 'product',
                    'sale_ok': True,
                    'purchase_ok': False,
                    'categ_id': order.categoria_envase_id.id,
                    'standard_price': order.costo_por_bote,
                    'list_price': order.precio_venta_por_bote,
                })
                _logger.info(f"Producto creado: {nuevo_producto.name} (ID {nuevo_producto.id})")

                # 🔹 Crea la lista de materiales (BoM)
                bom_ingredientes = self.env['mrp.bom'].create({
                    'product_tmpl_id': nuevo_producto.id,
                    'type': 'normal',
                    'bom_line_ids': [(0, 0, {
                        'product_id': ing.product_id.id,
                        'product_qty': ing.quantity_kg,
                    }) for ing in order.ingredientes_ids]
                })
                _logger.info(f"Lista de materiales de ingredientes creada: {bom_ingredientes.id}")

                # 🔹 Crea la lista de materiales para envasado
                bom_envases = self.env['mrp.bom'].create({
                    'product_tmpl_id': nuevo_producto.id,
                    'type': 'normal',
                    'bom_line_ids': [(0, 0, {
                        'product_id': env.product_id.id,
                        'product_qty': 1,
                    }) for env in order.envase_dynamic_lines]
                })
                _logger.info(f"Lista de materiales de envasado creada: {bom_envases.id}")

            except Exception as e:
                _logger.error(f"Error al crear el producto o la lista de materiales: {str(e)}")
                raise UserError(f"Error al crear el producto o la lista de materiales: {str(e)}")

        return super(SaleOrder, self).action_confirm()
    
    categoria_envase_id = fields.Many2one(
        'product.category',
        string="Tipo de Envase",
        domain="[('parent_id.name', '=', 'Envases')]"
    )

    envase_dynamic_lines = fields.One2many(
        'sale.order.envase.line',
        'order_id',
        string="Productos de Envasado Dinámicos"
    )

    @api.onchange('categoria_envase_id')
    def _onchange_categoria_envase(self):
        """Genera dinámicamente los campos de productos según las subcategorías de la categoría seleccionada."""
        if not self.categoria_envase_id:
            self.envase_dynamic_lines = [(5, 0, 0)]  # Borra los productos de envasado si no hay selección
            return

        subcategorias = self.env['product.category'].search([('parent_id', '=', self.categoria_envase_id.id)])
        
        nuevos_productos = []

        if not subcategorias:
            # Si NO hay subcategorías, creamos un solo campo para elegir productos de la categoría seleccionada
            productos = self.env['product.product'].search([('categ_id', '=', self.categoria_envase_id.id)])
            nuevos_productos.append((0, 0, {
                'categoria_id': self.categoria_envase_id.id,
                'name': self.categoria_envase_id.name,
                'product_id': productos[0].id if productos else False  # Si hay productos, toma el primero
            }))
        else:
            # Si hay subcategorías, creamos un campo por cada subcategoría y asignamos productos
            for subcat in subcategorias:
                productos = self.env['product.product'].search([('categ_id', '=', subcat.id)])
                nuevos_productos.append((0, 0, {
                    'categoria_id': subcat.id,
                    'name': subcat.name,
                    'product_id': productos[0].id if productos else False  # Si hay productos, toma el primero
                }))

        # Asignamos la nueva lista de productos dinámicamente
        self.envase_dynamic_lines = nuevos_productos

    costo_horas_fabricacion = fields.Float(string="Costo de Horas de Fabricación", compute="_compute_costo_fabricacion", store=True)
    costo_mezclado = fields.Float(string="Costo de Mezclado", compute="_compute_costo_mezclado", store=True)
    costo_transporte = fields.Float(string="Costo de Transporte", compute="_compute_costo_transporte", store=True)
    costo_impresion = fields.Float(string="Costo de Impresión", compute="_compute_costo_impresion", store=True)

    costo_por_bote = fields.Float(
        string="Costo por Bote",
        compute="_compute_costo_por_bote",
        store=True
    )
    precio_venta_por_bote = fields.Float(
        string="Precio de Venta por Bote",
        compute="_compute_precio_venta_por_bote",
        store=True
)
    margen_ganancia = fields.Float(string="Margen de Ganancia (%)", default=30.0)
    precio_final = fields.Float(string="Precio Final", compute="_compute_precio_final", store=True)

    @api.depends('ingredientes_ids')
    def _compute_costo_mezclado(self):
        for order in self:
            order.costo_mezclado = sum(ing.subtotal for ing in order.ingredientes_ids)
    
    

    @api.onchange('formulacion_template_id', 'num_capsulas_por_bote', 'num_botes')
    def _onchange_formulacion_template_id(self):
        """ Modifica las cantidades de los ingredientes sin duplicar líneas en la tabla. """
        if not self.formulacion_template_id:
            self.ingredientes_ids = [(5, 0, 0)]  # Si no hay plantilla, borrar ingredientes
            return

        ingredientes_dict = {line.product_id.id: line for line in self.ingredientes_ids}
        nuevos_ingredientes = []

        for line in self.formulacion_template_id.line_ids:
            cantidad_por_capsula_mg = line.quantity_per_capsule  # En mg
            cantidad_total_mg = cantidad_por_capsula_mg * self.num_capsulas_por_bote * self.num_botes
            cantidad_total_kg = cantidad_total_mg / 1_000_000  # 🔄 Convertir mg a kg

            if line.product_id.id in ingredientes_dict:
                # Si ya existe, actualizamos
                ingredientes_dict[line.product_id.id].quantity_per_capsule = cantidad_por_capsula_mg
                ingredientes_dict[line.product_id.id].quantity_kg = cantidad_total_kg
                ingredientes_dict[line.product_id.id].subtotal = cantidad_total_kg * line.product_id.list_price

                nuevos_ingredientes.append((1, ingredientes_dict[line.product_id.id].id, {
                    'quantity_per_capsule': cantidad_por_capsula_mg,
                    'quantity_kg': cantidad_total_kg,
                    'subtotal': cantidad_total_kg * line.product_id.list_price
                }))
            else:
                # Si no existe, lo agregamos
                nuevos_ingredientes.append((0, 0, {
                    'product_id': line.product_id.id,
                    'quantity_per_capsule': cantidad_por_capsula_mg,
                    'quantity_kg': cantidad_total_kg,
                    'price_unit': line.product_id.list_price,
                    'subtotal': cantidad_total_kg * line.product_id.list_price
                }))

        # Eliminar ingredientes que ya no deberían estar
        ingredientes_existentes = set(ingredientes_dict.keys())
        ingredientes_nuevos = set(line.product_id.id for line in self.formulacion_template_id.line_ids)
        ingredientes_a_eliminar = ingredientes_existentes - ingredientes_nuevos

        for product_id in ingredientes_a_eliminar:
            line_id = ingredientes_dict[product_id].id
            nuevos_ingredientes.append((2, line_id, 0))

        # Asignar ingredientes definitivos sin duplicaciones
        self.ingredientes_ids = nuevos_ingredientes

    @api.depends('ingredientes_ids')
    def _compute_costo_transporte(self):
        for order in self:
            order.costo_transporte = sum(ing.subtotal * 0.05 for ing in order.ingredientes_ids)

    @api.depends('num_capsulas_por_bote', 'num_botes')
    def _compute_costo_fabricacion(self):
        for order in self:
            order.costo_horas_fabricacion = (order.num_capsulas_por_bote * order.num_botes * 0.05) + (order.num_botes * 2.0)

    @api.depends('ingredientes_ids')
    def _compute_costo_impresion(self):
        for order in self:
            order.costo_impresion = sum(ing.subtotal * 0.02 for ing in order.ingredientes_ids)

    @api.depends('ingredientes_ids', 'num_capsulas_por_bote', 'num_botes')
    def _compute_costo_por_bote(self):
        for order in self:
            total_costo_ingredientes = sum(ing.subtotal for ing in order.ingredientes_ids)
            order.costo_por_bote = total_costo_ingredientes / order.num_botes if order.num_botes else 0.0
    


    @api.depends('costo_horas_fabricacion', 'costo_mezclado', 'costo_transporte', 'costo_impresion', 'margen_ganancia')
    def _compute_precio_final(self):
        for order in self:
            total_cost = (
                order.costo_horas_fabricacion +
                order.costo_mezclado +
                order.costo_transporte +
                order.costo_impresion
            )
            order.precio_final = total_cost * (1 + order.margen_ganancia / 100.0)

    def action_recalculate_costs(self):
        """ Botón para recalcular costos """
        self._compute_costo_fabricacion()
        self._compute_costo_mezclado()
        self._compute_costo_transporte()
        self._compute_costo_impresion()
        self._compute_precio_final()
    
    @api.depends('precio_final', 'num_botes')
    def _compute_precio_venta_por_bote(self):
        for order in self:
            order.precio_venta_por_bote = order.precio_final / order.num_botes if order.num_botes else 0.0

class SaleOrderEnvasado(models.Model):
    _name = 'sale.order.envasado'  # 🔥 Nombre correcto del modelo
    _description = "Envasado de Productos"

class SaleOrderEnvaseLine(models.Model):
    _name = 'sale.order.envase.line'
    _description = "Líneas dinámicas de selección de productos según envase"

    order_id = fields.Many2one('sale.order', string="Pedido Relacionado", ondelete='cascade')
    categoria_id = fields.Many2one('product.category', string="Categoría", required=True)
    name = fields.Char(string="Nombre de la Categoría")
    product_id = fields.Many2one(
        'product.product',
        string="Producto",
        domain="[('categ_id', '=', categoria_id)]"
    )
    
class SaleOrderIngredientes(models.Model):
    _name = 'sale.order.ingredientes'
    _description = "Línea de Ingredientes en la Formulación"

    order_id = fields.Many2one(
        comodel_name='sale.order',
        string="Pedido Relacionado",
        required=True,
        ondelete="cascade"
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Producto",
        required=True
    )

    quantity_per_capsule = fields.Float(string="Cantidad por Cápsula (mg)", required=True, default=0.0)  # ✅ Usamos el campo correcto
    quantity_kg = fields.Float(
        string="Cantidad Total (kg)", 
        compute="_compute_quantity_kg", 
        store=True
    )
    quantity = fields.Float(string="Cantidad", required=True, default=1.0)
    price_unit = fields.Float(string="PVP / UD.", related="product_id.list_price", readonly=True)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends('quantity_per_capsule', 'order_id.num_capsulas_por_bote', 'order_id.num_botes')
    def _compute_quantity_kg(self):
        """ Convierte la cantidad total de mg a kg """
        for line in self:
            if line.order_id:
                cantidad_total_mg = line.quantity_per_capsule * line.order_id.num_capsulas_por_bote * line.order_id.num_botes
                line.quantity_kg = cantidad_total_mg / 1_000_000  # 🔄 Convertir mg a kg

    @api.depends('quantity_kg', 'price_unit')
    def _compute_subtotal(self):
        """Calcula el subtotal con la cantidad total en kg"""
        for line in self:
            line.subtotal = line.quantity_kg * line.price_unit
