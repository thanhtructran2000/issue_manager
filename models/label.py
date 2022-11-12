from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class Label(models.Model):
    _name = 'label'
    _description = 'Label'

    name = fields.Char(string='Label', required="1")
    project_id = fields.Many2one('testing.project', string='Testing project', required="1")
