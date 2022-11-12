from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
class TestingProject(models.Model):
    _name = 'testing.project'
    _description = 'Dự án kiểm thử'
    _rec_name = 'project_name'
    _order = 'priority desc, start_date desc'
    # _transient = True
    # _log_access = True
    # INHERIT_ORDER = 'priority desc'

    project_name = fields.Char(string='Project name', required="1")
    manager_id = fields.Many2one('res.users', string="Project manager")
    start_date = fields.Date(string="Start date", default=fields.Date.today(), readonly=True)
    end_date = fields.Date(string="End date")
    assignee_id = fields.Many2one('res.users', string="Assignee",default=lambda self: self.env.user)
    description = fields.Html(string="Description")
    issues_ids = fields.One2many('issues', 'project_id')
    priority = fields.Selection([('0', ''), ('1', '')], default='0')
    issues_count = fields.Integer(compute='compute_count')
    label_ids = fields.One2many('label', 'project_id')

    def get_issue(self):
        for line in self:
            action = self.env.ref('issue_manager.action_issues').read()[0]
            action['domain'] = [('project_id', '=', line.id)]
            action['context'] = {'default_project_id': line.id}
            return action

    # def get_issue(self):
    #     self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'issues',
    #         'view_mode': 'tree',
    #         'res_model': 'issues',
    #         'domain': [('project_ids', '=', self.id)]
    #     }

    @api.depends('issues_ids')
    def compute_count(self):
        for record in self:
            record.issues_count = self.env['issues'].search_count(
                [('project_id', '=', record.id)])


    def unlink(self):
        if self.issues_count > 0:
            raise ValidationError(_("Dự án hiện tại vẫn còn đang có issue nên không thể xóa dự án kiểm thử"))
        return super(TestingProject, self).unlink()

    @api.constrains('start_date', 'end_date')
    def check_end_date(self):
        for record in self:
            if record.end_date < record.start_date:
                raise ValidationError(_("Ngày kết thúc không thể nhỏ hơn ngày bắt đầu"))

