# -*- coding: utf-8 -*-
{
    'name': "Issue manager",
    'summary': "Issue manager model",
    'description': """Information issue manager""",
    'author': "thanhtruc",
    'website': 'https://www.example.com',
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'base',
        'mail',
        'restful',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/issues_views.xml',
        'views/project.xml',
        'views/function_views.xml',
        'views/times_views.xml',
        'views/report_issues_views.xml',
        'wizard/update_state.xml',
        'views/report_project_list_xls_views.xml',
        'views/times_views.xml',
        'views/web_templates.xml',
        'views/testing_project_board_views.xml',
        'views/menu_views.xml',


    ],
    'external_dependencies': {
        'python': ['xlsxwriter', 'num2words', 'zxcvbn', 'paramiko', 'openpyxl', 'onesignal_sdk', 'docxtpl', 'docx',
                   'docxcompose'],
    },
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
}


