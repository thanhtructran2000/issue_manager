from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class ReportProjectListXls(models.TransientModel):
    _name = "report.project.list.xls"


    report_data = fields.Char('Name', size=256)
    file_name = fields.Binary('Excel Report', readonly=True)