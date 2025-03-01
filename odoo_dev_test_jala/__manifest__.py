# -*- coding: utf-8 -*-
{
    'name': "Odoo Dev Test Jala",

    'summary': """
        This module is created for the purpose of Odoo Development Test by JALA.
    """,

    'description': """
        This module is created for the purpose of Odoo Development Test by JALA.
    """,

    'author': "SHAFILAH AF",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/project_mgt_mail_template.xml',
        'views/project_management.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
