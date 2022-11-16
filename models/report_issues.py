from odoo import fields, models

class ReportIssues(models.TransientModel):
    _name = 'report.issues'

    report_data = fields.Char('Name', size=256)
    file_name = fields.Binary('Excel Report', readonly=True)