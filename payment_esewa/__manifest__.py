{
    "name": "esewa_payment",
    "author": "Siddhartha Sitaula",
    "version": "1.0.1.0.0",
    "category": "",
    'application': True,
    'sequence': 1,
    'depends': ['base','payment'],
    'data': [
        'views/payment_esewa_templates.xml',
        'data/payment_provider_data.xml',
        'views/payment_esewa_view.xml',
        # 'views/payment_esewa_transaction_views.xml'
    ],
}



