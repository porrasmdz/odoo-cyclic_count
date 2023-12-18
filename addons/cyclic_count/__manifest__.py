# -*- coding: utf-8 -*-
{
    'name': "Conteos Ciclicos",

    'summary': "Módulo de soporte para los conteos cíclicos",

    'description': """
Módulo de soporte del equipo de outsourcing de Excecon para optimizar y acelerar los conteos cíclicos
    """,

    'author': "ItsoGye",
    'website': "https://www.itso.ec",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [ 'base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/cyclic_count.xml',
        'views/product_category.xml',
        'views/company.xml',
        'views/product.xml',
        'views/warehouse.xml',
        'views/warehouse_type.xml',
        'views/subdivision_type.xml',
        'views/menu.xml',
    ],
   
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

