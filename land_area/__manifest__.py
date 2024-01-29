# -*- coding: utf-8 -*-
{
    'name': "land_area",

    'summary': """
        land_area""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    
    'assets': {
        'web.assets_backend': [
            'land_area/static/src/area_conversion/decimal.js',
            'land_area/static/src/area_conversion/RopaniBase.js',
            'land_area/static/src/area_conversion/KhatthaBase.js',
            'land_area/static/src/area_conversion/area_conversion.js',
            'land_area/static/src/area_conversion/area_conversion_view.js',
            'land_area/static/src/area_conversion/area_conversion_view.scss',
            'land_area/static/src/area_conversion/area_conversion_view.xml',  
            'land_area/static/src/House_area_conversion/house_area_conversion.js',
            'land_area/static/src/House_area_conversion/house_area_conversion.scss',
            'land_area/static/src/House_area_conversion/house_area_conversion.xml',
            'land_area/static/src/House_area_conversion/house_area_conversion_calc.js'
        ],
    },
    'license': 'LGPL-3',
}
