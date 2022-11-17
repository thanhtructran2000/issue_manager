# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class Times(models.Model):
    _name = 'times'
    _description = 'Times'

    times_name = fields.Integer(string='Times', required=True)
    start_date = fields.Date(string="Start date", default=fields.Date.today(), readonly=True)
    end_date = fields.Date(string="End date")
    assignee_id = fields.Many2one('res.users', string='Assignee', default=lambda self: self.env.user)
    project_id = fields.Many2one('testing.project', string='Project',  ondelete='cascade', required=True)

    @api.constrains('start_date', 'end_date')
    def check_end_date(self):
        for record in self:
            if record.end_date < record.start_date:
                raise ValidationError(_("Ngày kết thúc không thể nhỏ hơn ngày bắt đầu"))