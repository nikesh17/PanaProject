# -*- coding: utf-8 -*-
{
    'name': "Organization",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

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
    "sequence":2,

    # any module necessary for this one to work correctly
    'depends': ['base', "mail","web","website","upabhokta_samiti", "farmer", "nepali_date_widget", "nepali_typing"],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/organization_menu.xml',      
        'views/organization_information_view.xml',
        'views/organization_member.xml',
        'views/organization_purpose.xml',
        'views/organization_meeting_attendees.xml',
        'views/organization_fix_assets_view.xml',
        'views/organization_beneficiary.xml',
        # 'views/organization_renewal_detail.xml',
        'views/organization_program_detail.xml',
        'views/member_quota.xml',
        'views/organization_bhela_details.xml',
        
        'email_templates/verified_email_template.xml',
        'email_templates/insufficient_data_template.xml',
        'email_templates/rejected_email_template.xml',
        'reports/organization_pramad_patra.xml',
        'reports/program_schedule_report.xml',
        'reports/sastha_nabikaran_sifaris_report.xml',
        'reports/organization_detail_report.xml',
        'reports/new_organization_registration_report.xml',
        'reports/sanchalit karyakram_bibaran.xml',
    ],
   
}
