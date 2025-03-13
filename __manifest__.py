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
    'depends': ['base', 'mail', 'project', 'contacts'], #, 'stock'
    'data': [
        'security/ir.model.access.csv',
        'data/project_mgt_mail_template.xml',
        'views/project_management.xml',
        'views/trello_setup.xml',
        'views/project_project_inherit.xml',
        'views/project_task_type_inherit.xml',
        'views/project_task_inherit.xml',
        'views/res_partner_inherit.xml',
        'views/trello_logs.xml',
        'views/trello_webhook.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
