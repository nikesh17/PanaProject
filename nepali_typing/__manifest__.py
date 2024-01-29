# -*- coding: utf-8 -*-
{
    'name': "Nepali Preeti Typing",

    'summary': """
        Type in nepali font preeti""",

    'author': "Ardent Sharma",

    'category': "Localization/NepaliPreetiTyping",

    'license': 'LGPL-3',

    'version': '16.0.1.0',

    'depends': ['base', 'web', 'farmer'],

    'data':[
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/keyboards.xml',
        'views/user_preference.xml',
    ],

    'images': ['static/description/icon.png'],

    'assets': {
        'web.assets_backend': [
            '/nepali_typing/static/lib/*.js',
            '/nepali_typing/static/src/convert_to_nepali.js',
            '/nepali_typing/static/xml/language_menu.xml',
            # 'nepali_typing/static/src/keyboard_pref.js',
        ],
    },
}
