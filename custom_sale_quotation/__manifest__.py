
{
    'name': 'Barosa Custom Sale Quotation Enhancements',
    'version': '17.0.1.0',
    'summary': 'Enhancements in Sales Quotation for Cotizador and BoM Integration',
    'category': 'Sales',
    'author': 'Cristina M.',
    'license': 'LGPL-3',
    'depends': ['sale', 'mrp', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        # 'data/formulation_data.xml',
        # 'data/product_data.xml',
        'data/product_category_data.xml',
        'views/sale_order_views.xml',
        'views/product_template_views.xml',
        'views/formulation_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
