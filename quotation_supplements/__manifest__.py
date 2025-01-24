# -*- coding: utf-8 -*-
{
    'name': 'Cotización de Suplementos Alimenticios',
    'version': '1.0',
    'author': 'Cristina Martin',
    'summary': 'Gestión de cotizaciones para suplementos alimenticios.',
    'depends': ['sale', 'account', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/quotation_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
