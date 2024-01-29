# -*- coding: utf-8 -*-
{
    'name': "Nepali Datepicker Widget",

    'summary': """
        Date picker for nepali calendar""",

    'author': "Ardent Sharma",

    'category': "Localization/NepaliDatePicker",

    'license': 'LGPL-3',

    'price': '25.0',

    'currency': 'USD',

    'version': '16.0.1.0',

    'depends': ['base', 'web'],

    'images': ['static/description/banner_screenshot.png'],

    'assets': {
       'web.assets_backend': [
           '/nepali_date_widget/static/xml/date_field.xml',
           '/nepali_date_widget/static/xml/datetime_field.xml',
           '/nepali_date_widget/static/lib/nepaliDatePicker.css',
           '/nepali_date_widget/static/lib/nepaliDatePicker.js',
           '/nepali_date_widget/static/lib/custom_date_picker.js',
           '/nepali_date_widget/static/lib/nepali_date.js',
           '/nepali_date_widget/static/lib/nepali_datetime.js',
           '/nepali_date_widget/static/lib/message_inherit.js',
       ],
    },
}
