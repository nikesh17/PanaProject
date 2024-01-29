{
    'name': 'Product Portal',
    'author': 'Damodar Aryal and Utsab Bardewa',
    'category': 'Sales',
    'application':True,
    'sequence': 6,
    'summary': 'Portal Integration will empower users to see product counts easily, and maintain product templates easily, improving the overall sales process and customer experience',
    'depends': ['sale','website', 'portal','price_negotiation'],
    'images': [
        'static/description/cover.png',
    ],
    'data': [
        #security
        # "security/ir.model.access.csv",
        # "security/sale_security.xml",
        #views
        "views/portal_template.xml",
        # "views/portal_template_negotiation_approved.xml",
    ],
    'assets':{

        'web.assets_frontend':[
            'product_portal/static/src/js/portal_edit.js',

        ]
    },


    'license': 'LGPL-3'
}