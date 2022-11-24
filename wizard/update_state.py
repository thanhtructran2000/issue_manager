from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class UpdateState(models.TransientModel):
    _name = 'update.state'

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
    comment = fields.Text(string='Comment', required=True)


    def set_update_state(self):
        active_ids = self._context.get('active_ids', []) or []
        for record in self.env['issues'].browse(active_ids):
            record.status = self.status
            display_msg = """Stage change
                            <br/>
                            Stage: """ + record.status + """<br/>""" + str(self.comment)
            if record.status == 'resolved':
                record.bug_fix_date = fields.Date.today()

                th1 = self.env['times'].search([('project_id', '=', record.project_id.id), ('start_date', '<=', record.bug_fix_date), ('end_date', '>=', record.bug_fix_date)])
                th2 = self.env['times'].search([('project_id', '=', record.project_id.id), ('end_date', '<', record.bug_fix_date)], order='id desc', limit=1)
                if th1:
                    record.fixed_in_version = th1.times_name
                elif th2:
                    record.fixed_in_version = th2.times_name
                else:
                    record.fixed_in_version = record.times_id.times_name
            elif record.status != 'resolved':
                record.bug_fix_date = 0
                record.fixed_in_version = 0
            return record.message_post(body=display_msg)