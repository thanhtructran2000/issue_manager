from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
import base64
import io
import os
import copy
import xlsxwriter

class TestingProject(models.Model):
    _name = 'testing.project'
    _description = 'Dự án kiểm thử'
    _rec_name = 'project_name'
    _order = 'priority desc'


    project_name = fields.Char(string='Project name', required="1")
    project_code = fields.Char(string='Project code', required="1")
    manager_id = fields.Many2one('res.users', string="Project manager", default=lambda self: self.env.user)
    description = fields.Html(string="Description")
    priority = fields.Selection([('0', ''), ('1', '')], default='0')
    function_ids = fields.One2many('function', 'project_id')





    times_ids = fields.One2many('times', 'project_id')
    issues_ids = fields.One2many('issues', 'project_id')

    times_count = fields.Integer(compute='compute_count1')
    issues_count = fields.Integer(compute='compute_count2')

    issues_count_tong_loi = fields.Integer(compute='compute_count_tong_loi')


    # link đến danh sách các issues thuộc  1 project
    def get_issues(self):
        for line in self:
            action = self.env.ref('issue_manager.action_issues').read()[0]
            action['domain'] = [('project_id', '=', line.id)]
            action['context'] = {'default_project_id': line.id}
            return action


    # đếm số lượng issues trong 1 project
    @api.depends('issues_ids')
    def compute_count2(self):
        for record in self:
            record.issues_count = self.env['issues'].search_count(
                [('project_id', '=', record.id)])




    # link đến ds times thuộc project đó
    def get_times(self):
        for line in self:
            action = self.env.ref('issue_manager.action_times').read()[0]
            action['domain'] = [('project_id', '=', line.id)]
            action['context'] = {'default_project_id': line.id}
            return action

    # đếm số lần trong 1 project
    @api.depends('times_ids')
    def compute_count1(self):
        for record in self:
            record.times_count = self.env['times'].search_count(
                [('project_id', '=', record.id)])

    def unlink(self):
        if self.issues_count > 0:
            raise ValidationError(_("Dự án hiện tại vẫn còn đang có issue nên không thể xóa dự án kiểm thử"))
        return super(TestingProject, self).unlink()

    def download_file_import(self):
        cr = self.env.cr
        for line in self:

<<<<<<< HEAD
    # đếm số lượng issues có trạng thái new, open, onhold trong 1 project
    @api.depends('issues_ids')
    def compute_count_tong_loi(self):
        for record in self:
            record.issues_count_tong_loi = self.env['issues'].search_count(
                [('project_id', '=', record.id),
                 ('status', 'in', ('new', 'open', 'onhold')),
                 ])


=======
            custom_value = {}
            x = 0
            y = 0
            excel_style = {
                'tieude': {'bold': 1, 'font_name': 'Times New Roman', 'font_size': 15, 'align': 'center',
                           'valign': 'vcenter', 'text_wrap': 1},
                'tieude_font14': {'bold': 1, 'font_name': 'Times New Roman', 'font_size': 14, 'align': 'center',
                                  'valign': 'vcenter', 'text_wrap': 1},
                'header': {'border': 1, 'bold': 1, 'font_name': 'Times New Roman', 'font_size': 12, 'align': 'center',
                           'valign': 'vcenter', 'text_wrap': 1},
                'header_center': {'border': 1, 'bold': 1, 'font_name': 'Times New Roman', 'font_size': 13,
                                  'align': 'center', 'fg_color': '#D0cece', 'valign': 'vcenter', 'text_wrap': 1},
                'value': {'font_name': 'Times New Roman', 'font_size': 13, 'align': 'left'},
                'value_left': {'border': 1, 'font_name': 'Times New Roman', 'font_size': 12, 'align': 'left',
                               'valign': 'vcenter', 'text_wrap': 1},
                'value_left_bold': {'border': 1, 'bold': 1, 'font_name': 'Times New Roman', 'font_size': 14,
                                    'align': 'left',
                                    'valign': 'vcenter', 'text_wrap': 1},
                'value_left_italic': {'border': 1, 'italic': 1, 'font_name': 'Times New Roman', 'font_size': 12,
                                      'align': 'left',
                                      'valign': 'vcenter', 'text_wrap': 1},
                'value_left_underline': {'border': 1, 'underline': 1, 'font_name': 'Times New Roman', 'font_size': 12,
                                         'align': 'left', 'valign': 'vcenter', 'text_wrap': 1},
                'value_left_bold_italic': {'border': 1, 'bold': 1, 'italic': 1, 'font_name': 'Times New Roman',
                                           'font_size': 12,
                                           'align': 'left', 'valign': 'vcenter', 'text_wrap': 1},
                'value_left_bold_underline': {'border': 1, 'bold': 1, 'underline': 1, 'font_name': 'Times New Roman',
                                              'font_size': 12, 'align': 'left', 'valign': 'vcenter', 'text_wrap': 1},
                'value_left_bold_italic_underline': {'border': 1, 'bold': 1, 'italic': 1, 'underline': 1,
                                                     'font_name': 'Times New Roman', 'font_size': 12, 'align': 'left',
                                                     'valign': 'vcenter', 'text_wrap': 1},
                'value_left_no_border': {'border': 0, 'font_name': 'Times New Roman', 'font_size': 13, 'align': 'left',
                                         'valign': 'vcenter', 'text_wrap': 1},
                'value_left_bold_no_border': {'border': 0, 'bold': 1, 'font_name': 'Times New Roman', 'font_size': 14,
                                              'align': 'left', 'valign': 'vcenter', 'text_wrap': 1},
                'value_left_italic_no_border': {'border': 0, 'italic': 1, 'font_name': 'Times New Roman',
                                                'font_size': 12,
                                                'align': 'left', 'valign': 'vcenter', 'text_wrap': 1},
                'value_left_underline_no_border': {'border': 0, 'underline': 1, 'font_name': 'Times New Roman',
                                                   'font_size': 12,
                                                   'align': 'left', 'valign': 'vcenter', 'text_wrap': 1},
                'value_left_bold_italic_no_border': {'border': 0, 'bold': 1, 'italic': 1,
                                                     'font_name': 'Times New Roman',
                                                     'font_size': 12, 'align': 'left', 'valign': 'vcenter',
                                                     'text_wrap': 1},
                'value_left_bold_underline_no_border': {'border': 0, 'bold': 1, 'underline': 1,
                                                        'font_name': 'Times New Roman',
                                                        'font_size': 12, 'align': 'left', 'valign': 'vcenter',
                                                        'text_wrap': 1},
                'value_date': {'font_name': 'Times New Roman', 'font_size': 13, 'align': 'left',
                               'valign': 'vcenter', 'num_format': 'DD/MM/YYYY', 'text_wrap': 1},
                'value_date_border': {'border': 1, 'font_name': 'Times New Roman', 'font_size': 13, 'align': 'center',
                                      'valign': 'vcenter', 'num_format': 'DD/MM/YYYY', 'text_wrap': 1},
                'value_center': {'border': 1, 'font_name': 'Times New Roman', 'font_size': 13, 'align': 'center',
                                 'valign': 'vcenter', 'text_wrap': 1},
            }
            style = copy.deepcopy(excel_style)
            custom_value['worbook_name'] = line.project_code + "_" + line.project_name
            custom_value['tieude'] = "Thống kê kết quả kiểm định"
            workbook = xlsxwriter.Workbook(custom_value['worbook_name'])
            style_tieude = workbook.add_format(style['tieude'])
            style_header_bg = style['header_center']
            style_header_bg['fg_color'] = '#Ffcc99'
            style_header_bg1 = style['header']
            style_header_bg1['fg_color'] = '#D0cece'
            style_tieude_font_12 = style['tieude']
            style_tieude_font_12['font_size'] = 12
            # style_header_font_13 = style['header']
            # style_header_font_13['font_size'] = 13
            style_value_left_13 = style['value_left']
            style_value_left_13['font_size'] = 13
            style['header']["text_wrap"] = 1
            style_tieude_font14 = workbook.add_format(style['tieude_font14'])
            style_value_center = workbook.add_format(style['value_center'])
            style_header = workbook.add_format(style['header'])
            style_header_center = workbook.add_format(style['header_center'])
            style_value = workbook.add_format(style['value'])
            style_value_left = workbook.add_format(style['value_left'])
            style_value_left_bold = workbook.add_format(style['value_left_bold'])
            style_value_left_no_border = workbook.add_format(style['value_left_no_border'])
            style_value_left_bold_no_border = workbook.add_format(style['value_left_bold_no_border'])
            style_tieude = workbook.add_format(style['tieude'])
            style_tieude_font_12 = workbook.add_format(style_tieude_font_12)
            # style_header_font_13 = workbook.add_format(style_header_font_13)
            style_header_bg = workbook.add_format(style_header_bg)
            style_header_bg1 = workbook.add_format(style_header_bg1)
            style_value_left_13 = workbook.add_format(style_value_left_13)
            style_value_date = workbook.add_format(style['value_date'])
            style_value_date_border = workbook.add_format(style['value_date_border'])
            directory_path = os.path.dirname(os.path.join(os.path.dirname(__file__), "..", ".."))

            if len(str(line.id)) > 0:
                x = 0
                y = 0

                sheet = workbook.add_worksheet("ThongKe")
                sheet2 = workbook.add_worksheet("DanhSachChucNang")
                sheet3 = workbook.add_worksheet("DanhSachLoi")
                sheet4 = workbook.add_worksheet("SoLieu")

                # Thống kê lỗi
                sheet.set_row(x+1, 20)
                sheet.write(x+1, y+1, "THỐNG KÊ KẾT QUẢ KIỂM ĐỊNH LẦN …", style_tieude_font14)
                sheet.set_column(y + 1, y + 1, 63)
                sheet.set_column(y, y, 27)
                sheet.write(3, 0, "Tên dự án:", style_value_left_bold_no_border)
                sheet.write(3, 1, line.project_name, style_value_left_bold_no_border)
                sheet.write(4, 0, "Nội dung kiểm định:", style_value_left_bold_no_border)
                sheet.write(5, 0, "Kiểm định viên:", style_value_left_bold_no_border)
                # sheet.write(5, 1, line.assignee_id.name, style_value)
                sheet.write(6, 0, "Số lỗi trong lần ...:", style_value_left_bold_no_border)
                sheet.write(7, 0, "Tổng số lỗi:", style_value_left_bold_no_border)
                sheet.write(7, 1, line.issues_count, style_value)

                # Danh sách chức năng
                sheet2.set_column(0, 4, 35.5)
                sheet2.merge_range(1, 0, 1, 5, line.project_code + " - DANH SÁCH CHỨC NĂNG KIỂM ĐỊNH", style_tieude_font_12)
                sheet2.set_column(0, 0, 6.35)
                sheet2.merge_range(3, 0, 4, 0, "STT", style_header)
                sheet2.set_column(1, 1, 67.8)
                sheet2.merge_range(3, 1, 4, 1, "Chức năng kiểm định", style_header)
                sheet2.merge_range(3, 2, 3, 3, "Kết quả kiểm định", style_header)
                sheet2.set_column(2, 2, 13.5)
                sheet2.write(4, 2, "Giao diện", style_header)
                sheet2.set_column(3, 3, 13.5)
                sheet2.write(4, 3, "Chức năng", style_header)
                sheet2.set_column(4, 4, 15.5)
                sheet2.merge_range(3, 4, 4, 4, "Tổng issue", style_header)
                sheet2.set_column(5, 5, 35.5)
                sheet2.merge_range(3, 5, 4, 5, "Ghi chú", style_header)
                x = 5
                stt = 1
                for record in self.env['function'].search([('project_id', '=', line.id)]):
                    sheet2.write(x, 0, stt, style_value_center)
                    sheet2.write(x, 1, record.name, style_value_left)
                    sheet2.write(x, 2, "", style_value_left)
                    sheet2.write(x, 3, "", style_value_left)
                    sheet2.write(x, 5, "", style_value_left)
                    count_list = self.env['issues'].search([('function_id', '=', record.id)])
                    count = len(count_list)
                    sheet2.write(x, 4, count, style_value_center)

                    x += 1
                    stt += 1

                # Danh sách lỗi
                x = 4
                for record in self.env['issues'].search([('project_id', '=', line.id)]):
                    sheet3.write(x, 0, record.name, style_value_center) #ID
                    sheet3.write(x, 1, record.title, style_value_left) #Summary
                    sheet3.write(x, 2, record.function_id.name, style_value_center)  # Category
                    sheet3.write(x, 3, record.type, style_value_center)#Type
                    sheet3.write(x, 4, record.priority, style_value_center)#Severity
                    sheet3.write(x, 5, record.status, style_value_center)#Status
                    sheet3.write(x, 6, "", style_value_center)  #
                    sheet3.write(x, 7, "", style_value_center)  #
                    sheet3.write(x, 8, record.reporter_id.name, style_value_center)#Reporter
                    sheet3.write(x, 9, record.create_date, style_value_date_border)  # Bug report date
                    sheet3.write(x, 10, record.write_date, style_value_date_border)  # Bug fix date
                    sheet3.write(x, 11, "", style_value_center)  #
                    x += 1
                sheet3.merge_range(1, 0, 1, 6, line.project_code + " - THỐNG KÊ LỖI KIỂM ĐỊNH LẦN ...", style_tieude_font14)
                sheet3.set_column(0, 0, 5.55)
                sheet3.write(3, 0, "Bug ID", style_header_bg)


                sheet3.set_column(1, 1, 81.2)
                sheet3.write(3, 1, "Summary", style_header_bg)

                sheet3.set_column(2, 2, 23.6)
                sheet3.write(3, 2, "Category", style_header_bg)


                sheet3.set_column(3, 3, 14)
                sheet3.write(3, 3, "Type", style_header_bg)


                sheet3.set_column(4, 4, 9.4)
                sheet3.write(3, 4, "Severity", style_header_bg)

                sheet3.set_column(5, 5, 11.7)
                sheet3.write(3, 5, "Status", style_header_bg)

                sheet3.set_column(6, 6, 12.5)
                sheet3.write(3, 6, "Resolution", style_header_bg)

                sheet3.set_column(7, 7, 17.3)
                sheet3.write(3, 7, "Target Version", style_header_bg)

                sheet3.set_column(8, 8, 19.7)
                sheet3.write(3, 8, "Reporter", style_header_bg)

                sheet3.set_column(8, 8, 19.7)
                sheet3.write(3, 8, "Reporter", style_header_bg)

                sheet3.set_column(9, 9, 20.3)
                sheet3.write(3, 9, "Bug report date", style_header_bg)

                sheet3.set_column(9, 9, 18.9)
                sheet3.write(3, 9, "Bug report date", style_header_bg)

                sheet3.set_column(10, 10, 18.9)
                sheet3.write(3, 10, "Bug fix date", style_header_bg)

                sheet3.set_column(11, 11, 21)
                sheet3.write(3, 11, "Fixed in Version", style_header_bg)

                #Sheet số liệu
                sheet4.write(2, 1, self.env['issues'].search_count([('status', '=', 'new'),
                                    ('priority', '=', 'blocker'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(2, 2, self.env['issues'].search_count([('status', '=', 'open'),
                                    ('priority', '=', 'blocker'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(2, 3, self.env['issues'].search_count([('status', '=', 'resolved'),
                                    ('priority', '=', 'blocker'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(2, 4, self.env['issues'].search_count([('status', '=', 'invalid'),
                                    ('priority', '=', 'blocker'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(2, 5, self.env['issues'].search_count([('status', '=', 'duplicate'),
                                    ('priority', '=', 'blocker'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(2, 6, self.env['issues'].search_count([('status', '=', 'wontfix'),
                                    ('priority', '=', 'blocker'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(2, 7, self.env['issues'].search_count([('status', '=', 'close'),
                                    ('priority', '=', 'blocker'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(2, 8, '=sum(b3:h3)', style_value_center)

                sheet4.write(3, 1, self.env['issues'].search_count([('status', '=', 'new'),
                                    ('priority', '=', 'critical'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(3, 2, self.env['issues'].search_count([('status', '=', 'open'),
                                    ('priority', '=', 'critical'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(3, 3, self.env['issues'].search_count([('status', '=', 'resolved'),
                                    ('priority', '=', 'critical'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(3, 4, self.env['issues'].search_count([('status', '=', 'invalid'),
                                    ('priority', '=', 'critical'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(3, 5, self.env['issues'].search_count([('status', '=', 'duplicate'),
                                    ('priority', '=', 'critical'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(3, 6, self.env['issues'].search_count([('status', '=', 'wontfix'),
                                    ('priority', '=', 'critical'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(3, 7, self.env['issues'].search_count([('status', '=', 'close'),
                                    ('priority', '=', 'critical'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(3, 8, '=sum(b4:h4)', style_value_center)

                sheet4.write(4, 1, self.env['issues'].search_count([('status', '=', 'new'),
                                        ('priority', '=', 'major'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(4, 2, self.env['issues'].search_count([('status', '=', 'open'),
                                        ('priority', '=', 'major'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(4, 3, self.env['issues'].search_count([('status', '=', 'resolved'),
                                        ('priority', '=', 'major'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(4, 4, self.env['issues'].search_count([('status', '=', 'invalid'),
                                        ('priority', '=', 'major'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(4, 5, self.env['issues'].search_count([('status', '=', 'duplicate'),
                                        ('priority', '=', 'major'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(4, 6, self.env['issues'].search_count([('status', '=', 'wontfix'),
                                        ('priority', '=', 'major'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(4, 7, self.env['issues'].search_count([('status', '=', 'closed'),
                                        ('priority', '=', 'major'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(4, 8, '=sum(b5:h5)', style_value_center)

                sheet4.write(5, 1, self.env['issues'].search_count([('status', '=', 'new'),
                                        ('priority', '=', 'minor'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(5, 2, self.env['issues'].search_count([('status', '=', 'open'),
                                        ('priority', '=', 'minor'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(5, 3, self.env['issues'].search_count([('status', '=', 'resolved'),
                                        ('priority', '=', 'minor'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(5, 4, self.env['issues'].search_count([('status', '=', 'invalid'),
                                        ('priority', '=', 'minor'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(5, 5, self.env['issues'].search_count([('status', '=', 'duplicate'),
                                        ('priority', '=', 'minor'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(5, 6, self.env['issues'].search_count([('status', '=', 'wontfix'),
                                        ('priority', '=', 'minor'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(5, 7, self.env['issues'].search_count([('status', '=', 'close'),
                                        ('priority', '=', 'minor'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(5, 8, '=sum(b6:h6)', style_value_center)

                sheet4.write(6, 1, self.env['issues'].search_count([('status', '=', 'new'),
                                    111('priority', '=', 'trivial'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(6, 2, self.env['issues'].search_count([('status', '=', 'open'),
                                        ('priority', '=', 'trivial'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(6, 3, self.env['issues'].search_count([('status', '=', 'resolved'),
                                        ('priority', '=', 'trivial'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(6, 4, self.env['issues'].search_count([('status', '=', 'invalid'),
                                        ('priority', '=', 'trivial'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(6, 5, self.env['issues'].search_count([('status', '=', 'duplicate'),
                                        ('priority', '=', 'trivial'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(6, 6, self.env['issues'].search_count([('status', '=', 'wontfix'),
                                        ('priority', '=', 'trivial'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(6, 7, self.env['issues'].search_count([('status', '=', 'close'),
                                        ('priority', '=', 'trivial'), ('project_id', '=', line.id)]), style_value_center)
                sheet4.write(6, 8, '=sum(b7:h7)', style_value_center)

                sheet4.set_column(0, 0, 21.5)
                sheet4.write(1, 0, "By Severity", style_header_bg1)

                sheet4.set_column(1, 1, 11.5)
                sheet4.write(1, 1, "New", style_header_bg1)

                sheet4.set_column(2, 2, 11.5)
                sheet4.write(1, 2, "Open", style_header_bg1)

                sheet4.set_column(3, 3, 16.5)
                sheet4.write(1, 3, "Resolved", style_header_bg1)

                sheet4.set_column(4, 4, 12.8)
                sheet4.write(1, 4, "Invalid", style_header_bg1)

                sheet4.set_column(5, 5, 12.8)
                sheet4.write(1, 5, "Duplicate", style_header_bg1)

                sheet4.set_column(6, 6, 12.8)
                sheet4.write(1, 6, "Wontfix", style_header_bg1)

                sheet4.set_column(7, 7, 12.8)
                sheet4.write(1, 7, "Closed", style_header_bg1)

                sheet4.set_column(8, 8, 30.8)
                sheet4.write(1, 8, "Tổng cộng", style_header_bg1)

                sheet4.write(2, 0, "Blocker", style_value_left_13)
                sheet4.write(3, 0, "Critical", style_value_left_13)
                sheet4.write(4, 0, "Major", style_value_left_13)
                sheet4.write(5, 0, "Minor", style_value_left_13)
                sheet4.write(6, 0, "Trivial", style_value_left_13)

                sheet4.write(8, 0, "By Resolution", style_header_bg1)
                sheet4.write(8, 1, "New", style_header_bg1)
                sheet4.write(8, 2, "Open", style_header_bg1)
                sheet4.write(8, 3, "Resolved", style_header_bg1)
                sheet4.write(8, 4, "Invalid", style_header_bg1)
                sheet4.write(8, 5, "Duplicate", style_header_bg1)
                sheet4.write(8, 6, "Wontfix", style_header_bg1)
                sheet4.write(8, 7, "Closed", style_header_bg1)
                sheet4.write(8, 8, "Tổng cộng", style_header_bg1)

                x = 9
                y = 1
                sheet4.write(9, 0, "New", style_value_left_13)
                sheet4.write(10, 0, "Open", style_value_left_13)
                sheet4.write(11, 0, "On hold", style_value_left_13)
                sheet4.write(12, 0, "Close", style_value_left_13)

                # Xử lý chỗ trống
                x = 9
                y = 1
                sheet4.write(x, y, "", style_value_left)
                sheet4.write(x, y+1, "", style_value_left)
                sheet4.write(x, y+2, "", style_value_left)
                sheet4.write(x, y+3, "", style_value_left)
                sheet4.write(x, y+4, "", style_value_left)
                sheet4.write(x, y+5, "", style_value_left)
                sheet4.write(x, y+6, "", style_value_left)
                sheet4.write(x, y+7, "", style_value_left)

                x = 10
                y = 1
                sheet4.write(x, y, "", style_value_left)
                sheet4.write(x, y + 1, "", style_value_left)
                sheet4.write(x, y + 2, "", style_value_left)
                sheet4.write(x, y + 3, "", style_value_left)
                sheet4.write(x, y + 4, "", style_value_left)
                sheet4.write(x, y + 5, "", style_value_left)
                sheet4.write(x, y + 6, "", style_value_left)
                sheet4.write(x, y + 7, "", style_value_left)

                x = 11
                y = 1
                sheet4.write(x, y, "", style_value_left)
                sheet4.write(x, y + 1, "", style_value_left)
                sheet4.write(x, y + 2, "", style_value_left)
                sheet4.write(x, y + 3, "", style_value_left)
                sheet4.write(x, y + 4, "", style_value_left)
                sheet4.write(x, y + 5, "", style_value_left)
                sheet4.write(x, y + 6, "", style_value_left)
                sheet4.write(x, y + 7, "", style_value_left)

                sheet4.write(15, 0, "Tên dự án", style_value_left_no_border)
                sheet4.write(15, 1, line.project_name, style_value_left_no_border)
                sheet4.write(16, 0, "Giai đoạn test", style_value_left_no_border)
                sheet4.write(17, 0, "Lần", style_value_left_no_border)
                sheet4.write(18, 0, "Thời gian bắt đầu", style_value_left_no_border)

                sheet4.write(19, 0, "Thời gian kết thúc", style_value_left_no_border)

                sheet4.write(20, 0, "Lỗi trong lần ...", style_value_left_no_border)
                sheet4.write(21, 0, "Tổng số lỗi", style_value_left_no_border)
                sheet4.write(21, 1, line.issues_count, style_value_left_no_border)

                sheet.set_paper(9)  # set A4 as page format
                sheet2.set_paper(9)  # set A4 as page format
                pages_horz = 1
                pages_vert = 4
                sheet.fit_to_pages(pages_horz, pages_vert)

                sheet.set_margins(0, 0.7, 0.75, 0.75)
            workbook.close()
            fp = open(custom_value['worbook_name'], "rb")
            out = base64.encodestring(fp.read())
            attach_vals = {
                'report_data': custom_value['worbook_name'] + '.xlsx',
                'file_name': out,
            }
            act_id = self.env['report.issues'].create(attach_vals)
            fp.close()
            return {
                'type': 'ir.actions.act_url',
                'name': 'issues',
                'url': '/web/content/report.issues/%s/file_name/%s?download=true' % (
                    act_id.id, act_id.report_data),
            }
>>>>>>> parent of b055dcd (Merge pull request #12 from thanhtructran2000/su)

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
        custom_value['worbook_name'] = "Dự án kiểm định còn lỗi"
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
            sheet.write(x, 2, line.issues_count_tong_loi, style_value_center)
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

            sheet.write_url(1, 11, "internal:'Danh sách các dự án còn lỗi'!A1", string="Trở về",
                            cell_format=style_value_center_underline_no_border_gb_link)

            sheet.write(3,0, "Bug ID", style_value_center_bold_bg_2)
            sheet.write(3, 1, "Summary", style_value_center_bold_bg_2)
            sheet.write(3, 2, "Type", style_value_center_bold_bg_2)
            sheet.write(3, 3, "Severity", style_value_center_bold_bg_2)
            sheet.write(3, 4, "Status", style_value_center_bold_bg_2)




            sheet.write(3, 7, "Blocker", style_value_center_bold_bg_2)
            sheet.write(3, 8, "Critical", style_value_center_bold_bg_2)
            sheet.write(3, 9, "Major", style_value_center_bold_bg_2)
            sheet.write(3, 10, "Minor", style_value_center_bold_bg_2)
            sheet.write(3, 11, "Trivial", style_value_center_bold_bg_2)
            sheet.set_row(3, 40)


            x = 4
            for record in self.env['issues'].search([('project_id', '=', line.id), ('status','=', ('open', 'new', 'onhold'))]):
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
            sheet.write(4, 11, '=COUNTIF(D5:D500, L4)', style_value_right)

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
