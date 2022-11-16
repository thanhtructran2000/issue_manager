from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError



# tt



import base64
import io
import os
import copy
import xlsxwriter
# tt




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




# tt
    # mẫu xuất báo cáo cho tất cả các dự án kiểm định
    def download_file_import_1(self):
        excel_style = {
            'tieude': {'bold': 1, 'font_name': 'Calibri', 'font_size': 20, 'align': 'center',
                       'valign': 'vcenter', 'text_wrap': 1},
            'header': {'border': 1, 'bold': 1, 'font_name': 'Times New Roman', 'font_size': 12, 'align': 'center',
                       'valign': 'vcenter', 'text_wrap': 1},

            'value_center': {'border': 1, 'font_name': 'Calibri', 'font_size': 11, 'align': 'center',
                             'valign': 'vcenter', 'text_wrap': 1},

            'value_center_bold': {'border': 1, 'bold': 1, 'font_name': 'Calibri', 'font_size': 11,
                                  'align': 'center',
                                  'valign': 'vcenter', 'text_wrap': 1},

            'value_center_bold_no_border': {'border': 0, 'bold': 1, 'font_name': 'Calibri', 'font_size': 11,
                                  'align': 'center',
                                  'valign': 'vcenter', 'text_wrap': 1},

            'value_center_no_bold_no_border': {'border': 0, 'bold': 0, 'font_name': 'Calibri', 'font_size': 11,
                                            'align': 'center',
                                            'valign': 'vcenter', 'text_wrap': 1},

            'value_center_underline': {'border': 1, 'underline': 1, 'font_name': 'Calibri',
                                                 'font_size': 11,
                                                 'align': 'center', 'valign': 'vcenter', 'text_wrap': 1},

            'value_center_underline_no_border_gb_link': {'border': 0, 'underline': 1, 'font_name': 'Times New Roman',
                                                 'font_size': 12, 'fg_color': '#D0D3D4',
                                                 'align': 'center', 'valign': 'vcenter'},

            'value_left': {'border': 1, 'font_name': 'Calibri', 'font_size': 11, 'align': 'left',
                           'valign': 'vcenter',
                           'text_wrap': 1},
            'value_right': {'border': 1, 'font_name': 'Calibri', 'font_size': 11, 'align': 'right',
                            'valign': 'vcenter'},
        }

        cr = self.env.cr
        testing_projects = self.env['testing.project'].search([])
        custom_value = {}
        label_lst = []
        x = 0
        y = 0
        style = copy.deepcopy(excel_style)
        custom_value['worbook_name'] = "Mẫu xuất báo cáo cho tất cả các dự án kiểm định"
        custom_value['tieude'] = "Danh sách các dự án còn lỗi"
        workbook = xlsxwriter.Workbook(custom_value['worbook_name'])

        style['header']["text_wrap"] = 1
        style_tieude = workbook.add_format(style['tieude'])
        style_header = workbook.add_format(style['header'])

        style_value_center_bold = workbook.add_format(style['value_center_bold'])
        style_value_center_bold_bg_1 = style['value_center_bold']
        style_value_center_bold_bg_1['fg_color'] = '#707B7C'
        style_value_center_bold_bg_1 = workbook.add_format(style_value_center_bold_bg_1)

        style_value_center_bold_bg_2 = style['value_center_bold']
        style_value_center_bold_bg_2['fg_color'] = '#F5CBA7'
        style_value_center_bold_bg_2['font_name'] = 'Times New Roman'
        style_value_center_bold_bg_2['font_size'] = 12
        style_value_center_bold_bg_2 = workbook.add_format(style_value_center_bold_bg_2)


        style_value_center = workbook.add_format(style['value_center'])
        style_value_center_underline_no_border_gb_link = workbook.add_format(style['value_center_underline_no_border_gb_link'])
        style_value_left = workbook.add_format(style['value_left'])
        style_value_center_underline = workbook.add_format(style['value_center_underline'])

        style_value_center_underline_bg_link = style['value_center_underline']
        style_value_center_underline_bg_link['fg_color'] = '#EAEDED'
        style_value_center_underline_bg_link = workbook.add_format(style_value_center_underline_bg_link)

        style_value_center_bold_no_border = workbook.add_format(style['value_center_bold_no_border'])
        style_value_center_no_bold_no_border = workbook.add_format(style['value_center_no_bold_no_border'])
        style_value_right = workbook.add_format(style['value_right'])


        # tao sheet ds dự án còn lỗi
        sheet = workbook.add_worksheet("Danh sách các dự án còn lỗi")
        sheet.write(0, 1, "DANH SÁCH CÁC DỰ ÁN CÒN LỖI", style_tieude)
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 1, 70)
        sheet.set_column(2, 2, 10)
        sheet.set_row(0, 50)


        sheet.write(1, 0, "STT", style_value_center_bold_bg_1)
        sheet.write(1, 1, "TÊN DỰ ÁN", style_value_center_bold_bg_1)
        sheet.write(1, 2, "Tổng issue", style_value_center_bold_bg_1)
        sheet.write(1, 3, "", style_value_center_bold_bg_1)
        sheet.set_row(1, 30)


        x = 2
        stt = 1
        for line in testing_projects:
            sheet.write(x, 0, stt, style_value_center)
            sheet.write(x, 1, line.project_name, style_value_left)
            sheet.write(x, 2, line.issues_count, style_value_center)
            sheet.write_url(x, 3, "internal:'{}'!A1".format(line.project_name), string="»", cell_format=style_value_center_underline_bg_link)
            x += 1
            stt += 1
            # print_area(), set_paper() and fit_to_pages() do the trick
            sheet.print_area(0, 0, x, y)
            sheet.set_paper(9)  # set A4 as page format
            pages_horz = 1
            pages_vert = 4
            sheet.fit_to_pages(pages_horz, pages_vert)

            sheet.set_margins(0, 0.7, 0.75, 0.75)



        # tạo sheet cho từng dự án
        for line in testing_projects:
            sheet = workbook.add_worksheet(line.project_name)
            sheet.write(1, 1, line.project_name, style_tieude) # vd: HỘP KHÔNG GIẤY
            sheet.set_column(0, 0, 6)
            sheet.set_column(1, 1, 70)
            sheet.set_column(2, 2, 10)
            sheet.set_column(3, 3, 10)
            sheet.set_column(4, 4, 10)
            sheet.set_row(1, 25)

            sheet.write(1,2, "Tổng lỗi:", style_value_center_bold_no_border)
            sheet.write(1,3, '=COUNTA(A5:A100)', style_value_center_no_bold_no_border)

            sheet.write_url(1, 10, "internal:'Danh sách các dự án còn lỗi'!A1", string="Trở về",
                            cell_format=style_value_center_underline_no_border_gb_link)

            sheet.write(3,0, "Bug ID", style_value_center_bold_bg_2)
            sheet.write(3, 1, "Summary", style_value_center_bold_bg_2)
            sheet.write(3, 2, "Type", style_value_center_bold_bg_2)
            sheet.write(3, 3, "Severity", style_value_center_bold_bg_2)
            sheet.write(3, 4, "Status", style_value_center_bold_bg_2)
            sheet.write(3, 7, "Critical", style_value_center_bold_bg_2)
            sheet.write(3, 8, "Major", style_value_center_bold_bg_2)
            sheet.write(3, 9, "Minor", style_value_center_bold_bg_2)
            sheet.write(3, 10, "Trivial", style_value_center_bold_bg_2)
            sheet.set_row(3, 40)

            x = 4
            for record in self.env['issues'].search([('project_id', '=', line.id)]):
                sheet.write(x, 0, record.name, style_value_center)
                sheet.write_rich_string(x, 1, record.name, ": ", record.title, style_value_left)
                sheet.write(x, 2, record.type, style_value_center)
                sheet.write(x, 3, record.priority, style_value_center)
                sheet.write(x, 4, record.status, style_value_center)
                x+=1

            sheet.write(4, 7, '=COUNTIF(D5:D500, H4)', style_value_right)
            sheet.write(4, 8, '=COUNTIF(D5:D500, I4)', style_value_right)
            sheet.write(4, 9, '=COUNTIF(D5:D500, J4)', style_value_right)
            sheet.write(4, 10, '=COUNTIF(D5:D500, K4)', style_value_right)

            # hiển thị issue của dự án
            # print_area(), set_paper() and fit_to_pages() do the trick
            sheet.print_area(0, 0, x, y)
            sheet.set_paper(9)  # set A4 as page format
            pages_horz = 1
            pages_vert = 4
            sheet.fit_to_pages(pages_horz, pages_vert)



        workbook.close()
        fp = open(custom_value['worbook_name'], "rb")
        out = base64.encodestring(fp.read())
        attach_vals = {
            'report_data': custom_value['worbook_name'] + '.xlsx',
            'file_name': out,
        }
        act_id = self.env['report.project.list.xls'].create(attach_vals)
        fp.close()
        return {
            'type': 'ir.actions.act_url',
            'name': 'baocao',
            'url': '/web/content/report.project.list.xls/%s/file_name/%s?download=true' % (
                act_id.id, act_id.report_data),
        }


# kthuc tt
   