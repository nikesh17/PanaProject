# -*- coding: utf-8 -*-
{
    'name': "Tole Bikash",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Nikesh , Basanta",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'upabhokta_samiti',
                'web',
                'website',
                'auth_signup',
                'mail',
                'farmer',
                'nepali_date_widget',
                'nepali_typing'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'reports/tole_bikash_nibedan_report.xml',
        'reports/tole_bikash_meeting_report.xml',
        'reports/tole_bikash_member_position_report.xml',
        'reports/tole_bikash_rules_report.xml',
        'reports/tole_bikash_praman_patra_report.xml',

        'views/views.xml',
        'views/templates.xml',
        'views/tole_bikash_menu.xml',
        'views/tole_bikash_decision.xml',
        'views/tole_bikash_info.xml',
        'views/tole_bikash_members.xml',
        'views/tole_bikash_proposal.xml',
        'views/tole_bikash_attendees.xml',
        'views/tole_bikash_meeting_details.xml',
        'email_templates/insufficient_data_template.xml',
        'email_templates/rejected_email_template.xml',
        'email_templates/verified_email_template.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
