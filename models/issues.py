# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError



class Issues(models.Model):
    _name = "issues"
    _description = "Issues model"
    _inherit = ['mail.thread']


    name = fields.Char(string='ID', help="Result ID", readonly="1")
    title = fields.Char(string='Title', required=True, size=100)
    project_id = fields.Many2one('testing.project', string='Project',  ondelete='cascade', required=True)

    times_id = fields.Many2one('times', ondelete='cascade', required=True,  domain = "[('project_id', '=', project_id)]")

    description = fields.Text(string='Description')

    reproducible = fields.Selection(selection=[
        ('always', 'Always'),
        ('sometimes', 'Sometimes'),
        ('never','Never'),
    ], string='Reproducible',  default='always', required=True)
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

    function_id = fields.Many2one('function', string='Function', domain = "[('project_id', '=', project_id)]", ondelete='cascade')



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



































