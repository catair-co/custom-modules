# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import except_orm, UserError

class Analisis(models.Model):
    _name = "analisis_de_costes"
    _description = "Análisis de Costes"

    name = fields.Char(string='Nombre', required=True)
    user_id = fields.Many2one('res.users', string='Responsable',
        help="Usuario responsable/creador del análisis", default=lambda self: self.env.user,
        ondelete="cascade", index=True, required=True)
    notes = fields.Html(string='Notas')
    activo = fields.Boolean(string='Activo')


    cliente = fields.Many2one('res.partner', string='Cliente',
        help="Cliente solicitante del producto del análisis",
        ondelete="cascade", index=True, required=True)
    nombre_producto = fields.Char(string='Nombre Producto')
    fecha = fields.Date(string='Fecha')
    aplicacion = fields.Char(string='Aplicación')
    pais = fields.Many2one('res.country', string='País', default=68,
                           ondelete="cascade", index=True, required=True)
    comentarios = fields.Html(string='Comentarios')
    fecha_lanzamiento = fields.Date(string='Fecha de lanzamiento')
    producto_existente = fields.Boolean(string='Producto existente')
    unidades_pedido = fields.Integer(string='Unidades por pedido')
    unidades_anual = fields.Integer(string='Unidades anuales')
    currency_id = fields.Many2one('res.currency', string='Moneda', default=1,
                                  ondelete="cascade", index=True, required=True)
    precio_target = fields.Monetary(string='Precio target', help='Precio objetivo')
    velocidad_encapsulado = fields.Selection([('5000', '5000'),
                                    ('10000', '10000'),
                                    ('15000', '15000'),
                                    ('20000', '20000'),
                                    ('25000', '25000'),
                                    ('30000', '30000')], string='Velocidad encapsulado')
    velocidad_envasado = fields.Selection([('200', '200'),
                                    ('300', '300'),
                                    ('400', '400'),
                                    ('500', '500')], string='Velocidad envasado')
    merma_estimada = fields.Selection([('2', '2'),
                                    ('3', '3'),
                                    ('4', '4'),
                                    ('5', '5')], string='Merma estimada (%)')
    tipo_limpieza = fields.Selection([('0,5', '0,5'),
                                    ('1', '1'),
                                    ('2', '2')], string='Tipo limpieza')

    packaging_primario = fields.Selection([('blister', 'Blister'),
                                           ('pildorero', 'Pildorero'),
                                           ('granel', 'Granel'),
                                           ('bote', 'Bote')], string='Packaging primario')
    tamanyo_blister = fields.Selection([('86', '86mm x 63mm 15 caps sin troquel (Tamaño 1, 0)'),
                                        ('85', '85mm x 75mm 10 caps lote troquelado (Tamaño 1, 0)'),
                                        ('85b', '85mm x 75mm 15 caps lote troquelado (Tamaño 1, 0, 00)'),
                                        ('93', '93mm x 67mm 15 caps lote troquelado (Tamaño 1, 0, 00)'),
                                        ('110', '110mm x 75mm 15 caps sin troquel (Tamaño 1, 0, 00)')],
                                        string='Tamaño blister')
    blister_unidad = fields.Integer(string='Blister unidad')
    serigrafia = fields.Boolean(string='Serigrafía')
    bobina_aluminio = fields.Selection([('if3', 'Impresión IF3'),
                                           ('cliente', 'Impresión cliente')], string='Bobina aluminio')
    tamanyo_pet = fields.Selection([('50', '50'),
                                    ('75', '75'),
                                    ('100', '100'),
                                    ('150', '150'),
                                    ('200', '200'),
                                    ('250', '250'),
                                    ('300', '300'),
                                    ('500', '500')], string='Tamaño Pet')
    tapa = fields.Selection([('rosca', 'Rosca'),
                             ('presion', 'Presión')], string='Tapa')
    loteado = fields.Selection([('tapa', 'Tapa'),
                             ('base', 'Base')], string='Loteado')
    color = fields.Selection([('bl', 'BL'),
                              ('tr', 'TR'),
                              ('ambar', 'Ámbar'),
                              ('otro', 'Otro')], string='Color')
    etiqueta = fields.Selection([('si', 'Sí'),
                                 ('no', 'No'),
                                 ('cliente', 'Impresión cliente')], string='Etiqueta')

    # Packaging secundario
    estuche = fields.Selection([('si', 'Sí'),
                                 ('no', 'No'),
                                 ('cliente', 'Cliente')], string='Estuche')
    especificaciones_estuche = fields.Char(string='Especificaciones Estuche')
    prospecto = fields.Selection([('si', 'Sí'),
                                 ('no', 'No'),
                                 ('cliente', 'Impresión cliente')], string='Prospecto')
    formato_lote = fields.Selection([('if3', 'Aporta IF3'),
                                     ('cliente', 'Aporta cliente')], string='Formato Lote')

    # Galénica
    galenica = fields.Selection([('capsula', 'Cápsula'),
                                 ('comprimidos', 'Comprimidos'),
                                 ('polvo', 'Polvo'),
                                 ('otros', 'Otros')], string='Galénica')
    producto_galenica = fields.Many2one('product.template', string='Tipo de cápsula',
        ondelete="cascade", index=True, required=False, domain="[('name', '=like', 'CA %')]")
    unidad_por_envase = fields.Selection([('30', '30'),
                                          ('60', '60'),
                                          ('90', '90'),
                                          ('120', '120'),
                                          ('180', '180'),
                                          ('300', '300')], string='Unidad por envase')
    lote = fields.Selection([('if3', 'Propio IF3'),
                             ('cliente', 'Propio  cliente')], string='Lote')
    analisis_especiales = fields.Selection([('si', 'Sí'),
                                            ('no', 'No'),
                                            ('propia', 'Impresión propia')], string='Análisis especiales')
    especificar_analitica = fields.Char(string='Especificar Analítica')
    # Ingredientes
    ingredientes_ids = fields.One2many('analisis_de_costes.ingredientes', 'analisis_de_costes_id',
                                       string='Ingredientes de Análisis de Costes')
    # Excipientes
    excipientes_ids = fields.One2many('analisis_de_costes.excipientes', 'analisis_de_costes_id',
                                       string='Excipientes de Análisis de Costes')
    # Otros
    aspecto_visual = fields.Char(string='Aspecto Visual')
    limitacion_excipientes = fields.Char(string='Limitación Excipientes')

    ## INGREDIENTES
    ## 1
    ingred_origen1 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente1 = fields.Many2one('product.template')
    ingred_mg_unitaria1 = fields.Integer()
    fuente1 = fields.Char()
    vrn1 = fields.Boolean()
    marca1 = fields.Char()
    alternativa1 = fields.Boolean()
    ingred_proveedor1 = fields.Many2one('res.partner')
    ingred_precio1 = fields.Monetary()
    ## 2
    ingred_origen2 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente2 = fields.Many2one('product.template')
    ingred_mg_unitaria2 = fields.Integer()
    fuente2 = fields.Char()
    vrn2 = fields.Boolean()
    marca2 = fields.Char()
    alternativa2 = fields.Boolean()
    ingred_proveedor2 = fields.Many2one('res.partner')
    ingred_precio2 = fields.Monetary()
    ## 3
    ingred_origen3 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente3 = fields.Many2one('product.template')
    ingred_mg_unitaria3 = fields.Integer()
    fuente3 = fields.Char()
    vrn3 = fields.Boolean()
    marca3 = fields.Char()
    alternativa3 = fields.Boolean()
    ingred_proveedor3 = fields.Many2one('res.partner')
    ingred_precio3 = fields.Monetary()
    ## 4
    ingred_origen4 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente4 = fields.Many2one('product.template')
    ingred_mg_unitaria4 = fields.Integer()
    fuente4 = fields.Char()
    vrn4 = fields.Boolean()
    marca4 = fields.Char()
    alternativa4 = fields.Boolean()
    ingred_proveedor4 = fields.Many2one('res.partner')
    ingred_precio4 = fields.Monetary()
    ## 5
    ingred_origen5 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente5 = fields.Many2one('product.template')
    ingred_mg_unitaria5 = fields.Integer()
    fuente5 = fields.Char()
    vrn5 = fields.Boolean()
    marca5 = fields.Char()
    alternativa5 = fields.Boolean()
    ingred_proveedor5 = fields.Many2one('res.partner')
    ingred_precio5 = fields.Monetary()
    ## 6
    ingred_origen6 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente6 = fields.Many2one('product.template')
    ingred_mg_unitaria6 = fields.Integer()
    fuente6 = fields.Char()
    vrn6 = fields.Boolean()
    marca6 = fields.Char()
    alternativa6 = fields.Boolean()
    ingred_proveedor6 = fields.Many2one('res.partner')
    ingred_precio6 = fields.Monetary()
    ## 7
    ingred_origen7 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente7 = fields.Many2one('product.template')
    ingred_mg_unitaria7 = fields.Integer()
    fuente7 = fields.Char()
    vrn7 = fields.Boolean()
    marca7 = fields.Char()
    alternativa7 = fields.Boolean()
    ingred_proveedor7 = fields.Many2one('res.partner')
    ingred_precio7 = fields.Monetary()
    ## 8
    ingred_origen8 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente8 = fields.Many2one('product.template')
    ingred_mg_unitaria8 = fields.Integer()
    fuente8 = fields.Char()
    vrn8 = fields.Boolean()
    marca8 = fields.Char()
    alternativa8 = fields.Boolean()
    ingred_proveedor8 = fields.Many2one('res.partner')
    ingred_precio8 = fields.Monetary()
    ## 9
    ingred_origen9 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente9 = fields.Many2one('product.template')
    ingred_mg_unitaria9 = fields.Integer()
    fuente9 = fields.Char()
    vrn9 = fields.Boolean()
    marca9 = fields.Char()
    alternativa9 = fields.Boolean()
    ingred_proveedor9 = fields.Many2one('res.partner')
    ingred_precio9 = fields.Monetary()
    ## 10
    ingred_origen10 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente10 = fields.Many2one('product.template')
    ingred_mg_unitaria10 = fields.Integer()
    fuente10 = fields.Char()
    vrn10 = fields.Boolean()
    marca10 = fields.Char()
    alternativa10 = fields.Boolean()
    ingred_proveedor10 = fields.Many2one('res.partner')
    ingred_precio10 = fields.Monetary()
    ## 11
    ingred_origen11 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente11 = fields.Many2one('product.template')
    ingred_mg_unitaria11 = fields.Integer()
    fuente11 = fields.Char()
    vrn11 = fields.Boolean()
    marca11 = fields.Char()
    alternativa11 = fields.Boolean()
    ingred_proveedor11 = fields.Many2one('res.partner')
    ingred_precio11 = fields.Monetary()
    ## 12
    ingred_origen12 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente12 = fields.Many2one('product.template')
    ingred_mg_unitaria12 = fields.Integer()
    fuente12 = fields.Char()
    vrn12 = fields.Boolean()
    marca12 = fields.Char()
    alternativa12 = fields.Boolean()
    ingred_proveedor12 = fields.Many2one('res.partner')
    ingred_precio12 = fields.Monetary()
    ## 13
    ingred_origen13 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente13 = fields.Many2one('product.template')
    ingred_mg_unitaria13 = fields.Integer()
    fuente13 = fields.Char()
    vrn13 = fields.Boolean()
    marca13 = fields.Char()
    alternativa13 = fields.Boolean()
    ingred_proveedor13 = fields.Many2one('res.partner')
    ingred_precio13 = fields.Monetary()
    ## 14
    ingred_origen14 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente14 = fields.Many2one('product.template')
    ingred_mg_unitaria14 = fields.Integer()
    fuente14 = fields.Char()
    vrn14 = fields.Boolean()
    marca14 = fields.Char()
    alternativa14 = fields.Boolean()
    ingred_proveedor14 = fields.Many2one('res.partner')
    ingred_precio14 = fields.Monetary()
    ## 15
    ingred_origen15 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente15 = fields.Many2one('product.template')
    ingred_mg_unitaria15 = fields.Integer()
    fuente15 = fields.Char()
    vrn15 = fields.Boolean()
    marca15 = fields.Char()
    alternativa15 = fields.Boolean()
    ingred_proveedor15 = fields.Many2one('res.partner')
    ingred_precio15 = fields.Monetary()
    ## 16
    ingred_origen16 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente16 = fields.Many2one('product.template')
    ingred_mg_unitaria16 = fields.Integer()
    fuente16 = fields.Char()
    vrn16 = fields.Boolean()
    marca16 = fields.Char()
    alternativa16 = fields.Boolean()
    ingred_proveedor16 = fields.Many2one('res.partner')
    ingred_precio16 = fields.Monetary()
    ## 17
    ingred_origen17 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente17 = fields.Many2one('product.template')
    ingred_mg_unitaria17 = fields.Integer()
    fuente17 = fields.Char()
    vrn17 = fields.Boolean()
    marca17 = fields.Char()
    alternativa17 = fields.Boolean()
    ingred_proveedor17 = fields.Many2one('res.partner')
    ingred_precio17 = fields.Monetary()
    ## 18
    ingred_origen18 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente18 = fields.Many2one('product.template')
    ingred_mg_unitaria18 = fields.Integer()
    fuente18 = fields.Char()
    vrn18 = fields.Boolean()
    marca18 = fields.Char()
    alternativa18 = fields.Boolean()
    ingred_proveedor18 = fields.Many2one('res.partner')
    ingred_precio18 = fields.Monetary()
    ## 19
    ingred_origen19 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente19 = fields.Many2one('product.template')
    ingred_mg_unitaria19 = fields.Integer()
    fuente19 = fields.Char()
    vrn19 = fields.Boolean()
    marca19 = fields.Char()
    alternativa19 = fields.Boolean()
    ingred_proveedor19 = fields.Many2one('res.partner')
    ingred_precio19 = fields.Monetary()
    ## 20
    ingred_origen20 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente20 = fields.Many2one('product.template')
    ingred_mg_unitaria20 = fields.Integer()
    fuente20 = fields.Char()
    vrn20 = fields.Boolean()
    marca20 = fields.Char()
    alternativa20 = fields.Boolean()
    ingred_proveedor20 = fields.Many2one('res.partner')
    ingred_precio20 = fields.Monetary()
    ## 21
    ingred_origen21 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente21 = fields.Many2one('product.template')
    ingred_mg_unitaria21 = fields.Integer()
    fuente21 = fields.Char()
    vrn21 = fields.Boolean()
    marca21 = fields.Char()
    alternativa21 = fields.Boolean()
    ingred_proveedor21 = fields.Many2one('res.partner')
    ingred_precio21 = fields.Monetary()
    ## 22
    ingred_origen22 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente22 = fields.Many2one('product.template')
    ingred_mg_unitaria22 = fields.Integer()
    fuente22 = fields.Char()
    vrn22 = fields.Boolean()
    marca22 = fields.Char()
    alternativa22 = fields.Boolean()
    ingred_proveedor22 = fields.Many2one('res.partner')
    ingred_precio22 = fields.Monetary()
    ## 23
    ingred_origen23 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente23 = fields.Many2one('product.template')
    ingred_mg_unitaria23 = fields.Integer()
    fuente23 = fields.Char()
    vrn23 = fields.Boolean()
    marca23 = fields.Char()
    alternativa23 = fields.Boolean()
    ingred_proveedor23 = fields.Many2one('res.partner')
    ingred_precio23 = fields.Monetary()
    ## 24
    ingred_origen24 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente24 = fields.Many2one('product.template')
    ingred_mg_unitaria24 = fields.Integer()
    fuente24 = fields.Char()
    vrn24 = fields.Boolean()
    marca24 = fields.Char()
    alternativa24 = fields.Boolean()
    ingred_proveedor24 = fields.Many2one('res.partner')
    ingred_precio24 = fields.Monetary()
    ## 25
    ingred_origen25 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente25 = fields.Many2one('product.template')
    ingred_mg_unitaria25 = fields.Integer()
    fuente25 = fields.Char()
    vrn25 = fields.Boolean()
    marca25 = fields.Char()
    alternativa25 = fields.Boolean()
    ingred_proveedor25 = fields.Many2one('res.partner')
    ingred_precio25 = fields.Monetary()
    ## 26
    ingred_origen26 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente26 = fields.Many2one('product.template')
    ingred_mg_unitaria26 = fields.Integer()
    fuente26 = fields.Char()
    vrn26 = fields.Boolean()
    marca26 = fields.Char()
    alternativa26 = fields.Boolean()
    ingred_proveedor26 = fields.Many2one('res.partner')
    ingred_precio26 = fields.Monetary()
    ## 27
    ingred_origen27 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente27 = fields.Many2one('product.template')
    ingred_mg_unitaria27 = fields.Integer()
    fuente27 = fields.Char()
    vrn27 = fields.Boolean()
    marca27 = fields.Char()
    alternativa27 = fields.Boolean()
    ingred_proveedor27 = fields.Many2one('res.partner')
    ingred_precio27 = fields.Monetary()
    ## 28
    ingred_origen28 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente28 = fields.Many2one('product.template')
    ingred_mg_unitaria28 = fields.Integer()
    fuente28 = fields.Char()
    vrn28 = fields.Boolean()
    marca28 = fields.Char()
    alternativa28 = fields.Boolean()
    ingred_proveedor28 = fields.Many2one('res.partner')
    ingred_precio28 = fields.Monetary()
    ## 29
    ingred_origen29 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente29 = fields.Many2one('product.template')
    ingred_mg_unitaria29 = fields.Integer()
    fuente29 = fields.Char()
    vrn29 = fields.Boolean()
    marca29 = fields.Char()
    alternativa29 = fields.Boolean()
    ingred_proveedor29 = fields.Many2one('res.partner')
    ingred_precio29 = fields.Monetary()
    ## 30
    ingred_origen30 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente30 = fields.Many2one('product.template')
    ingred_mg_unitaria30 = fields.Integer()
    fuente30 = fields.Char()
    vrn30 = fields.Boolean()
    marca30 = fields.Char()
    alternativa30 = fields.Boolean()
    ingred_proveedor30 = fields.Many2one('res.partner')
    ingred_precio30 = fields.Monetary()
    ## 31
    ingred_origen31 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente31 = fields.Many2one('product.template')
    ingred_mg_unitaria31 = fields.Integer()
    fuente31 = fields.Char()
    vrn31 = fields.Boolean()
    marca31 = fields.Char()
    alternativa31 = fields.Boolean()
    ingred_proveedor31 = fields.Many2one('res.partner')
    ingred_precio31 = fields.Monetary()
    ## 32
    ingred_origen32 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente32 = fields.Many2one('product.template')
    ingred_mg_unitaria32 = fields.Integer()
    fuente32 = fields.Char()
    vrn32 = fields.Boolean()
    marca32 = fields.Char()
    alternativa32 = fields.Boolean()
    ingred_proveedor32 = fields.Many2one('res.partner')
    ingred_precio32 = fields.Monetary()
    ## 33
    ingred_origen33 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente33 = fields.Many2one('product.template')
    ingred_mg_unitaria33 = fields.Integer()
    fuente33 = fields.Char()
    vrn33 = fields.Boolean()
    marca33 = fields.Char()
    alternativa33 = fields.Boolean()
    ingred_proveedor33 = fields.Many2one('res.partner')
    ingred_precio33 = fields.Monetary()
    ## 34
    ingred_origen34 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente34 = fields.Many2one('product.template')
    ingred_mg_unitaria34 = fields.Integer()
    fuente34 = fields.Char()
    vrn34 = fields.Boolean()
    marca34 = fields.Char()
    alternativa34 = fields.Boolean()
    ingred_proveedor34 = fields.Many2one('res.partner')
    ingred_precio34 = fields.Monetary()
    ## 35
    ingred_origen35 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente35 = fields.Many2one('product.template')
    ingred_mg_unitaria35 = fields.Integer()
    fuente35 = fields.Char()
    vrn35 = fields.Boolean()
    marca35 = fields.Char()
    alternativa35 = fields.Boolean()
    ingred_proveedor35 = fields.Many2one('res.partner')
    ingred_precio35 = fields.Monetary()
    ## 36
    ingred_origen36 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente36 = fields.Many2one('product.template')
    ingred_mg_unitaria36 = fields.Integer()
    fuente36 = fields.Char()
    vrn36 = fields.Boolean()
    marca36 = fields.Char()
    alternativa36 = fields.Boolean()
    ingred_proveedor36 = fields.Many2one('res.partner')
    ingred_precio36 = fields.Monetary()
    ## 37
    ingred_origen37 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente37 = fields.Many2one('product.template')
    ingred_mg_unitaria37 = fields.Integer()
    fuente37 = fields.Char()
    vrn37 = fields.Boolean()
    marca37 = fields.Char()
    alternativa37 = fields.Boolean()
    ingred_proveedor37 = fields.Many2one('res.partner')
    ingred_precio37 = fields.Monetary()
    ## 38
    ingred_origen38 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente38 = fields.Many2one('product.template')
    ingred_mg_unitaria38 = fields.Integer()
    fuente38 = fields.Char()
    vrn38 = fields.Boolean()
    marca38 = fields.Char()
    alternativa38 = fields.Boolean()
    ingred_proveedor38 = fields.Many2one('res.partner')
    ingred_precio38 = fields.Monetary()
    ## 39
    ingred_origen39 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente39 = fields.Many2one('product.template')
    ingred_mg_unitaria39 = fields.Integer()
    fuente39 = fields.Char()
    vrn39 = fields.Boolean()
    marca39 = fields.Char()
    alternativa39 = fields.Boolean()
    ingred_proveedor39 = fields.Many2one('res.partner')
    ingred_precio39 = fields.Monetary()
    ## 40
    ingred_origen40 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente40 = fields.Many2one('product.template')
    ingred_mg_unitaria40 = fields.Integer()
    fuente40 = fields.Char()
    vrn40 = fields.Boolean()
    marca40 = fields.Char()
    alternativa40 = fields.Boolean()
    ingred_proveedor40 = fields.Many2one('res.partner')
    ingred_precio40 = fields.Monetary()
    ## 41
    ingred_origen41 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente41 = fields.Many2one('product.template')
    ingred_mg_unitaria41 = fields.Integer()
    fuente41 = fields.Char()
    vrn41 = fields.Boolean()
    marca41 = fields.Char()
    alternativa41 = fields.Boolean()
    ingred_proveedor41 = fields.Many2one('res.partner')
    ingred_precio41 = fields.Monetary()
    ## 42
    ingred_origen42 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente42 = fields.Many2one('product.template')
    ingred_mg_unitaria42 = fields.Integer()
    fuente42 = fields.Char()
    vrn42 = fields.Boolean()
    marca42 = fields.Char()
    alternativa42 = fields.Boolean()
    ingred_proveedor42 = fields.Many2one('res.partner')
    ingred_precio42 = fields.Monetary()
    ## 43
    ingred_origen43 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente43 = fields.Many2one('product.template')
    ingred_mg_unitaria43 = fields.Integer()
    fuente43 = fields.Char()
    vrn43 = fields.Boolean()
    marca43 = fields.Char()
    alternativa43 = fields.Boolean()
    ingred_proveedor43 = fields.Many2one('res.partner')
    ingred_precio43 = fields.Monetary()
    ## 44
    ingred_origen44 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente44 = fields.Many2one('product.template')
    ingred_mg_unitaria44 = fields.Integer()
    fuente44 = fields.Char()
    vrn44 = fields.Boolean()
    marca44 = fields.Char()
    alternativa44 = fields.Boolean()
    ingred_proveedor44 = fields.Many2one('res.partner')
    ingred_precio44 = fields.Monetary()
    ## 45
    ingred_origen45 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente45 = fields.Many2one('product.template')
    ingred_mg_unitaria45 = fields.Integer()
    fuente45 = fields.Char()
    vrn45 = fields.Boolean()
    marca45 = fields.Char()
    alternativa45 = fields.Boolean()
    ingred_proveedor45 = fields.Many2one('res.partner')
    ingred_precio45 = fields.Monetary()
    ## 46
    ingred_origen46 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente46 = fields.Many2one('product.template')
    ingred_mg_unitaria46 = fields.Integer()
    fuente46 = fields.Char()
    vrn46 = fields.Boolean()
    marca46 = fields.Char()
    alternativa46 = fields.Boolean()
    ingred_proveedor46 = fields.Many2one('res.partner')
    ingred_precio46 = fields.Monetary()
    ## 47
    ingred_origen47 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente47 = fields.Many2one('product.template')
    ingred_mg_unitaria47 = fields.Integer()
    fuente47 = fields.Char()
    vrn47 = fields.Boolean()
    marca47 = fields.Char()
    alternativa47 = fields.Boolean()
    ingred_proveedor47 = fields.Many2one('res.partner')
    ingred_precio47 = fields.Monetary()
    ## 48
    ingred_origen48 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente48 = fields.Many2one('product.template')
    ingred_mg_unitaria48 = fields.Integer()
    fuente48 = fields.Char()
    vrn48 = fields.Boolean()
    marca48 = fields.Char()
    alternativa48 = fields.Boolean()
    ingred_proveedor48 = fields.Many2one('res.partner')
    ingred_precio48 = fields.Monetary()
    ## 49
    ingred_origen49 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente49 = fields.Many2one('product.template')
    ingred_mg_unitaria49 = fields.Integer()
    fuente49 = fields.Char()
    vrn49 = fields.Boolean()
    marca49 = fields.Char()
    alternativa49 = fields.Boolean()
    ingred_proveedor49 = fields.Many2one('res.partner')
    ingred_precio49 = fields.Monetary()
    ## 50
    ingred_origen50 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    ingrediente50 = fields.Many2one('product.template')
    ingred_mg_unitaria50 = fields.Integer()
    fuente50 = fields.Char()
    vrn50 = fields.Boolean()
    marca50 = fields.Char()
    alternativa50 = fields.Boolean()
    ingred_proveedor50 = fields.Many2one('res.partner')
    ingred_precio50 = fields.Monetary()

    ## EXCIPIENTES
    ## 1
    excipi_origen1 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    excipiente1 = fields.Many2one('product.template')
    excipi_mg_unitaria1 = fields.Integer()
    excipi_proveedor1 = fields.Many2one('res.partner')
    excipi_precio1 = fields.Monetary()
    ## 2
    excipi_origen2 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    excipiente2 = fields.Many2one('product.template')
    excipi_mg_unitaria2 = fields.Integer()
    excipi_proveedor2 = fields.Many2one('res.partner')
    excipi_precio2 = fields.Monetary()
    ## 3
    excipi_origen3 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    excipiente3 = fields.Many2one('product.template')
    excipi_mg_unitaria3 = fields.Integer()
    excipi_proveedor3 = fields.Many2one('res.partner')
    excipi_precio3 = fields.Monetary()
    ## 4
    excipi_origen4 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    excipiente4 = fields.Many2one('product.template')
    excipi_mg_unitaria4 = fields.Integer()
    excipi_proveedor4 = fields.Many2one('res.partner')
    excipi_precio4 = fields.Monetary()
    ## 5
    excipi_origen5 = fields.Selection([('if3lab', 'IF3Lab'), ('cliente', 'Cliente')])
    excipiente5 = fields.Many2one('product.template')
    excipi_mg_unitaria5 = fields.Integer()
    excipi_proveedor5 = fields.Many2one('res.partner')
    excipi_precio5 = fields.Monetary()

    @api.onchange('merma_estimada', 'unidades_pedido', 'unidad_por_envase')
    def _onchange_precio_proveedor(self):
        supplier_info = self.env['product.supplierinfo']
        for ingrediente in self.ingredientes_ids:
            if ingrediente.ingrediente:
                # Solo buscaremos los precios de proveedor que tengan una cantidad mínima distinta de 0
                try:
                    # Esta fórmula viene del Excel, de las celdas 'Qty total necesaria'
                    min_cantidad = (ingrediente.mg_unitaria * (1 + int(self.merma_estimada)) *
                                    self.unidades_pedido * int(
                                    self.unidad_por_envase) / 1000000)
                except:
                    min_cantidad = 0

                supplier = supplier_info.search([('product_tmpl_id', '=' , ingrediente.ingrediente.id),
                                        ('name', '=', ingrediente.proveedor.id),
                                        ('min_qty', '<=', min_cantidad)],
                                        order = 'min_qty desc')

                if supplier:
                    #if supplier[0].min_qty > min_cantidad:
                    precio = supplier[0].price
                    #if supplier[1].min_qty > min_cantidad:
                    #    precio = supplier[1].price
                    #precio = 0
                    #for linea in supplier:
                    #    if min_cantidad >= linea.min_qty:
                    #        precio = linea.price
                    #        break
                    ingrediente.price = precio
                else:
                    ingrediente.price = 0



class AnalisisIngredientes(models.Model):
    _name = "analisis_de_costes.ingredientes"
    _description = "Ingredientes de Análisis de Costes"

    # # establecemos domain para filtrar el proveedor dependiendo del producto
    # #@api.model
    # def _set_domain_for_supplier(self):
    #     import pdb
    #     pdb.set_trace()
    #     #fiscal_country_ids = self.env['account.fiscal.position'].search([('company_id', '=', self.env.company.id), ('foreign_vat', '!=', False)]).country_id.ids
    #     #return [('tag_name', '!=', None), '|', ('report_id.country_id', '=', self.env.company.country_id.id), ('report_id.country_id', 'in', fiscal_country_ids)]
    #     class_obj =self.env['product.supplierinfo'].search([('product_tmpl_id', '=', self.ingrediente.id)])
    #     print("*************************************************************************************************************************")
    #     print(self.ingrediente.id)
    #     supplier_list = []
    #     for data in class_obj:
    #         supplier_list.append(data.name.id)

    #     res = {}
    #     res['domain'] = {'proveedor': [('id', 'in', supplier_list)]}
    #     # res['domain'] = {'proveedor': [('id', 'in', [10])]}
    #     #return res
    #     #return [('proveedor', 'in', supplier_list)]

    #     #self.proveedor = res
    #     #self.proveedor = [('proveedor', 'in', [10])]
    #     return [('id', 'in', supplier_list)]

    origen = fields.Selection([('if3lab', 'IF3Lab'),
                               ('cliente', 'Cliente')], string='Origen')
    ingrediente = fields.Many2one('product.template', string='Ingrediente',
        ondelete="cascade", index=True, required=False, domain="['|','|',('name', '=like', 'ES %'),"
                                                               "('name', '=like', 'VM %'),"
                                                               "('name', '=like', 'MP %')]")
    mg_unitaria = fields.Integer(string='mg/unitaria')
    fuente = fields.Char(string='Fuente')
    vrn = fields.Boolean(string='VRN')
    marca = fields.Char(string='Marca')
    alternativa = fields.Boolean(string='Alternativa posible')
    # domain="[('id', 'in', 10)]"  -  , domain=_set_domain_for_supplier
    proveedor = fields.Many2one('res.partner', string='Proveedor',
            ondelete="cascade", index=True, required=False)
    analisis_de_costes_id = fields.Many2one('analisis_de_costes', string='Análisis ID')
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
        default=lambda self: self.env.company)
    company_currency_id = fields.Many2one(related='company_id.currency_id')
    price = fields.Monetary(
        string='Precio',
        currency_field='company_currency_id',
    )
    
    @api.onchange('ingrediente', 'proveedor', 'mg_unitaria')
    def _onchange_proveedor(self):
        supplier_info = self.env['product.supplierinfo']
        supplier = supplier_info.search([('product_tmpl_id', '=' , self.ingrediente.id),
                                        ('name', '=', self.proveedor.id)],
                                        order = 'min_qty desc')
        if supplier:
            try:
                # Esta fórmula viene del Excel, de las celdas 'Qty total necesaria'
                min_cantidad = (self.mg_unitaria * (1 + int(self.analisis_de_costes_id.merma_estimada)) *
                                self.analisis_de_costes_id.unidades_pedido * int(
                                self.analisis_de_costes_id.unidad_por_envase) / 1000000)
            except:
                min_cantidad = 0

            precio = 0
            for linea in supplier:
                if min_cantidad >= linea.min_qty:
                    precio = linea.price
                    break
            self.price = precio
        else:
            self.price = 0

class AnalisisExcipientes(models.Model):
    _name = "analisis_de_costes.excipientes"
    _description = "Excipientes de Análisis de Costes"

    origen = fields.Selection([('if3lab', 'IF3Lab'),
                               ('cliente', 'Cliente')], string='Origen')
    excipiente = fields.Many2one('product.template', string='Excipiente',
        ondelete="cascade", index=True, required=False, domain="[('name', '=like', 'MP %')]")
    mg_unitaria = fields.Integer(string='mg/unitaria')
    proveedor = fields.Many2one('res.partner', string='Proveedor',
        ondelete="cascade", index=True, required=False)
    analisis_de_costes_id = fields.Many2one('analisis_de_costes', string='Análisis ID')
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
        default=lambda self: self.env.company)
    company_currency_id = fields.Many2one(related='company_id.currency_id')
    price = fields.Monetary(
        string='Precio',
        currency_field='company_currency_id',
    )

    @api.onchange('excipiente', 'proveedor', 'mg_unitaria')
    def _onchange_proveedor(self):
        supplier_info = self.env['product.supplierinfo']
        supplier = supplier_info.search([('product_tmpl_id', '=' , self.excipiente.id),
                                        ('name', '=', self.proveedor.id)],
                                        order='min_qty desc')
        if supplier:
            try:
                # Esta fórmula viene del Excel, de las celdas 'Qty total necesaria'
                min_cantidad = (self.mg_unitaria * (1 + int(self.analisis_de_costes_id.merma_estimada)) *
                                self.analisis_de_costes_id.unidades_pedido * int(
                                self.analisis_de_costes_id.unidad_por_envase) / 1000000)
            except:
                min_cantidad = 0

            precio = 0
            for linea in supplier:
                if min_cantidad >= linea.min_qty:
                    precio = linea.price
                    break
            self.price = precio
        else:
            self.price = 0