# -*- coding: utf-8 -*-
{
    'name': "Custom Purchase Order Dates",

    'summary': """
        Customize purchase order and picking dates""",

    'description': """
        Customize purchase order and picking dates
    """,

    "author": "",
    # "website": "",
    'category': 'Purchase',
    'version': '15.0.1',
    'depends': ['base', 'purchase', 'stock', 'product_expiry'],
    'data': [
        'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
         'views/stock_quant.xml',
         'wizard/expired_movement_wizard.xml',
    ],
    'icon': 'indaws_custom_purchase_order_dates/static/description/icon.png',
    'installable': True,
    'application': True,
    'auto_install': False,
}
