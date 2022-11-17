# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class Times(models.Model):
    _name = 'times'
    _description = 'Times'
    _rec_name = 'times_name' #

    times_name = fields.Integer(required=True, default=False, readonly=True)
    start_date = fields.Date(string="Start date", default=fields.Date.today(), readonly=True)
    end_date = fields.Date(string="End date")
    assignee_id = fields.Many2one('res.users', string='Assignee', default=lambda self: self.env.user)
    project_id = fields.Many2one('testing.project', string='Project',  ondelete='cascade', required=True)

    issues_ids = fields.One2many('issues', 'times_id')

    count_issues_times = fields.Integer(compute='count_issues_of_times')



    # link đến danh sách các issues thuộc times đó
    def get_issues_of_times(self):
        for line in self:
            action = self.env.ref('issue_manager.action_issues').read()[0]
            action['domain'] = [('times_id', '=', line.id)]
            action['context'] = {'default_times_id': line.id,
                                 'default_project_id': line.project_id.id,
                                 }
            return action




    # đếm số lượng issues trong 1 times
    @api.depends('issues_ids')
    def count_issues_of_times(self):
        for record in self:
            record.count_issues_times = self.env['issues'].search_count(
                [('times_id', '=', record.id)])



    @api.constrains('start_date', 'end_date')
    def check_end_date(self):
        for record in self:
            if record.end_date < record.start_date:
                raise ValidationError(_("Ngày kết thúc không thể nhỏ hơn ngày bắt đầu"))