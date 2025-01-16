# -*- coding: utf-8 -*-
{
    'name': "Análisis de costes",
    'summary': """
        Análisis de costes para if3Lab, para enlazar con Hojas de Cálculo .""",
    'description': """
        Contiene:
            - creación de campos necesarios (50 para ingredientes y 5 para excipientes)
            - creación de menú, acción y vistas: el tree contiene cada campo del modelo
        NO Contiene:
            - acción automatizada 'Análisis- Guardar lineas Ingredientes y Excipientes' para pasar líneas a campos
            - acción automatizada 'Análisis activo y responsable' para tener un solo análisis activo y poner por defecto el responsable
            - acción automatizada 'Análisis - cambio precios proveedor' que modifica los precios de los ingredientes y excipientes cuando cambia la tarifa de proveedor
    """,
    'version': '17.0.0.1',
    # 'author': "",
    # 'website': "",
    'category': 'Customization',
    'license': 'OPL-1',
    'depends': ['base', 'sale', 'documents'],
    'data': [
        'security/ir.model.access.csv',
        'views/analisis_costes.xml',
    ],
    # 'icon': 'indaws_custom_purchase_order_dates/static/description/icon_indaws.png',
    'application': False,
}
