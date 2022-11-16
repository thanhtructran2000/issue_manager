from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class Function(models.Model):
    _name = 'function'
    _description = 'Function'

    name = fields.Char(string='Function', required="1")
    project_id = fields.Many2one('testing.project', string='Testing project', required="1", ondelete='cascade')
    issues_count = fields.Integer(string='Issues', compute='issues_count2')


    def issues_count2(self):
        for record in self:
            record.issues_count = self.env['issues'].search_count(
                [('function_id', '=', record.id)])