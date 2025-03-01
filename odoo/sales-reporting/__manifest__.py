# -*- coding: utf-8 -*-
{
    'name': "sales-reporting",

    'summary': """
        A module to generate sales reports filtering by date and customer""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Powersoft",
    'website': "https://www.pcl.co.tz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/sales_reporting_views.xml',
        'views/sales_reporting_wizard_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
