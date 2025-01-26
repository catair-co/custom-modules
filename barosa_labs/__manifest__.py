{
    'name': 'Barosa Labs',
    'version': '1.3',
    'summary': 'Gestión completa de presupuestos, formulaciones y proyectos para Barosa Labs.',
    'category': 'Custom',
    'author': 'Usuario',
    'depends': ['sale', 'product', 'project'],
    'data': [
        'views/formulation_template_view.xml',
        'views/sale_order_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}