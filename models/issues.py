# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class Issues(models.Model):
    _name = "issues"
    _description = "Issues model"
    _inherit = ['mail.thread']

    name = fields.Char(string='ID', help="Result ID", readonly="1")
    title = fields.Char(string='Title', required=True, size=100)
    project_id = fields.Many2one('testing.project', string='Project', ondelete='cascade', required=True)

    times_id = fields.Many2one('times', ondelete='cascade', required=True, domain="[('project_id', '=', project_id)]")

    description = fields.Text(string='Description')

    reproducible = fields.Selection(selection=[
        ('always', 'Always'),
        ('sometimes', 'Sometimes'),
        ('never', 'Never'),
    ], string='Reproducible', default='always', required=True)
    type = fields.Selection(selection=[
        ('bug', 'Bug'),
        ('enhancement', 'Enhancement'),
        ('proposal', 'Proposal'),
        ('task', 'Task'),
    ], string='Type', default='bug', required=True)
    priority = fields.Selection(selection=[
        ('blocker', 'Blocker'),
        ('critical', 'Critical'),
        ('major', 'Major'),
        ('minor', 'Minor'),
        ('trivial', 'Trivial')
    ], string='Priority', required=True)

    # attachment_ids = fields.Many2many('ir.attachment', 'issues_attachments_rel', 'issues_id',
    #                                   'attachment_id', 'Attachments')
    reporter_id = fields.Many2one('res.users', string='Reporter', required=True, default=lambda self: self.env.user)
    assignee_id = fields.Many2one('res.users', string='Assignee', default=lambda self: self.env.user)

    status = fields.Selection(selection=[
        ('new', 'New'),
        ('open', 'Open'),
        ('onhold', 'On hold'),
        ('resolved', 'Resolved'),
        ('duplicate', 'Duplicate'),
        ('wontfix', 'Wontfix'),
        ('invalid', 'Invalid'),
        ('closed', 'Closed'),
    ], string='Status', default='new', required=True)

    resolution = fields.Selection(selection=[
        ('new', 'New'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('onhold', 'On hold'),
    ], string='Resolution', default='new', required=True)

    function_id = fields.Many2one('function', string='Function', domain="[('project_id', '=', project_id)]",
                                  ondelete='cascade')

    bug_fix_date = fields.Date(string='Bug fix date')
    fixed_in_version = fields.Integer(string='Fixed in version')

    @api.model
    def create(self, vals):

        if self.env['issues'].search([], order='id desc'):
            last_name = self.env['issues'].search([], order='id desc')[0].name
            new_name = last_name.split('#')
            new_name = int(new_name[1]) + 1
            vals['name'] = '#' + str(new_name)
        else:
            vals['name'] = '#1'
        return super(Issues, self).create(vals)

    # quyền
    def unlink(self):
        if self.reporter_id.id != self.env.user.id:
            raise UserError(_("You do not have permission to delete"))
        else:
            return super(Issues, self).unlink()

    def update_state(self):
        self.ensure_one()
        import_obj = self.env['update.state']
        new_import = import_obj.create({})
        action = self.env.ref('issue_manager.action_update_state').read()[0]
        action.update({
            'res_id': new_import.id,
        })
        return action

    # dashboard issues

    @api.model
    def get_dashboard_data_issues(self, project_id):
        issues_list = []
        # tổng issues của 1 project
        projects = self.search([('project_id', '=', project_id)])
        # tổng issues còn lỗi của 1 project
        tong_lois = projects.filtered(lambda x: x.status in ('open', 'new', 'onhold'))

        for record in tong_lois:
            issues_list.append({'name': record.name,
                                'title': record.title,
                                'type': record.type,
                                'priority': record.priority,
                                'status': record.status, })

        # bieu do status
        opens = projects.filtered(lambda x: x.status == 'open')
        news = projects.filtered(lambda x: x.status == 'new')
        onholds = projects.filtered(lambda x: x.status == 'onhold')
        resolveds = projects.filtered(lambda x: x.status == 'resolved')
        duplicates = projects.filtered(lambda x: x.status == 'duplicate')
        wontfixs = projects.filtered(lambda x: x.status == 'wontfix')
        invalids = projects.filtered(lambda x: x.status == 'invalid')
        closeds = projects.filtered(lambda x: x.status == 'closed')

        # các issues blocker trong ds các dự án còn lỗi
        issues_of_blocker = tong_lois.filtered(lambda x: x.priority == 'blocker')
        issues_blocker_list = []
        for record in issues_of_blocker:
            issues_blocker_list.append({'name': record.name,
                                        'title': record.title,
                                        'type': record.type,
                                        'priority': record.priority,
                                        'status': record.status, })

        # các issues critical trong ds các dự án còn lỗi
        issues_of_critical = tong_lois.filtered(lambda x: x.priority == 'critical')
        issues_critical_list = []
        for record in issues_of_critical:
            issues_critical_list.append({'name': record.name,
                                         'title': record.title,
                                         'type': record.type,
                                         'priority': record.priority,
                                         'status': record.status, })

        # các issues major trong ds các dự án còn lỗi
        issues_of_major = tong_lois.filtered(lambda x: x.priority == 'major')
        issues_major_list = []
        for record in issues_of_major:
            issues_major_list.append({'name': record.name,
                                      'title': record.title,
                                      'type': record.type,
                                      'priority': record.priority,
                                      'status': record.status, })
        # các issues minor trong ds các dự án còn lỗi
        issues_of_minor = tong_lois.filtered(lambda x: x.priority == 'minor')
        issues_minor_list = []
        for record in issues_of_minor:
            issues_minor_list.append({'name': record.name,
                                      'title': record.title,
                                      'type': record.type,
                                      'priority': record.priority,
                                      'status': record.status, })
        # các issues trivial trong ds các dự án còn lỗi
        issues_of_trivial = tong_lois.filtered(lambda x: x.priority == 'trivial')
        issues_trivial_list = []
        for record in issues_of_trivial:
            issues_trivial_list.append({'name': record.name,
                                        'title': record.title,
                                        'type': record.type,
                                        'priority': record.priority,
                                        'status': record.status, })

        # biểu đồ times


        search_times_of_project = projects.project_id.times_ids
        times_list = []
        issues_of_times_list = []
        # tìm số lần trong 1 project, số issue trong lần đó
        for record in search_times_of_project:
            times_list.append(record.times_name)
            issues_of_times_list.append(record.count_issues_times)

        # biểu đồ function
        search_function_of_project = projects.project_id.function_ids
        function_list = []
        issues_of_function_list = []
        for record in search_function_of_project:
            function_list.append(record.name)
            issues_of_function_list.append(record.issues_count)

        # biểu đồ issues còn lỗi và issues closed
        phan_tram_issues_con_loi = (100 // len(projects)) * len(tong_lois)
        phan_tram_issues_closed = 100 - phan_tram_issues_con_loi

        return {'table_tong_loi_body': issues_list,
                'table_tong_loi_count': len(tong_lois),
                # ds các issues blocker
                'table_blocker_body': issues_blocker_list,
                'table_blocker_count': len(issues_of_blocker),
                # ds các issues critical
                'table_critical_body': issues_critical_list,
                'table_critical_count': len(issues_of_critical),
                # ds các issues major
                'table_major_body': issues_major_list,
                'table_major_count': len(issues_of_major),
                # ds các issues minor
                'table_minor_body': issues_minor_list,
                'table_minor_count': len(issues_of_minor),
                # ds các issues trivial
                'table_trivial_body': issues_trivial_list,
                'table_trivial_count': len(issues_of_trivial),

                # status biểu đồ

                'pie_chart_label': ["Open", "New", "On hold", "Resolved", "Duplicate", "Wontfix", "Invalid", "Closed"],
                'pie_chart_value': [len(opens), len(news), len(onholds), len(resolveds), len(duplicates), len(wontfixs),
                                    len(invalids), len(closeds)],
                'pie_chart_color': ['#ebbf80', '#4c73b3', '#e38634', '#f42828', '#dcdfe9',
                                    'rgba(255, 99, 132)', 'rgba(75, 192, 192)', 'rgba(153, 102, 255)'],

                # function
                'bar_chart_1_label': [*function_list],
                'bar_chart_1_value': [*issues_of_function_list],
                'bar_chart_1_color': ['#a6b9ef', '#28a745', 'rgba(255, 205, 86)',
                                      'rgba(75, 192, 192)', 'rgba(153, 102, 255)'],

                # biểu đồ issues bug vs issues closed
                'doughnut_label': ['Issues bug', 'Issues closed'],
                'doughnut_value': [phan_tram_issues_con_loi, phan_tram_issues_closed],
                'doughnut_color': ['#24bcfe', '#f5803f'],
                # times

                'bar_chart_label': [
                    *times_list
                ],

                'bar_chart_value': [*issues_of_times_list],
                'bar_chart_color': ['rgba(255, 99, 132)', 'rgba(255, 159, 64)', 'rgba(255, 205, 86)',
                                    'rgba(75, 192, 192)', 'rgba(153, 102, 255)'],
                }
