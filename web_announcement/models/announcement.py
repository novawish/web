# Copyright 2019 Dong Duc, DAO
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Announcement(models.Model):
    _name = "announcement"

    name = fields.Char(required=True)
    popup_title = fields.Char()
    popup_message = fields.Text()
    active = fields.Boolean(default=True)
    date_from = fields.Datetime()
    date_to = fields.Datetime()
    notify_type = fields.Selection([
            ('success', 'SUCCESS'),
            ('danger', 'DANGER'),
            ('warning', 'WARNING'),
            ('info', 'INFO'),
            ('default', 'DEFAULT'),
        ], string="Popup Type", default='default',
        help="Type will define the color of the Announcements"
    )
    is_always_show = fields.Boolean(
        string="Always display",
        help="Always display the popup on screen",
        default=True
    )
    notify_all_users = fields.Boolean(
        string="Notify all users",
        help="Check if you want to notify all users",
        default=False
    )
    user_ids = fields.Many2many(
        'res.users', 'announcement_res_users_rel', 'aid', 'uid')
    group_ids = fields.Many2many(
        'res.groups', 'announcement_res_groups_rel', 'aid', 'gid')

    @api.model
    def check_is_announced(self, user_id):
        for anm in self.search([]):
            now = fields.Datetime.now()
            if ((anm.date_from and now < anm.date_from)
                    or (anm.date_to and now > anm.date_to)):
                continue
            user = self.env['res.users'].browse(user_id)
            if (anm.notify_all_users
                    or user in anm.user_ids
                    or user in anm.group_ids.mapped('users')):
                user._notify_channel(
                    type_message=anm.notify_type,
                    message=anm.popup_message,
                    title=anm.popup_title,
                    sticky=anm.is_always_show,
                )

    @api.multi
    def _get_users(self):
        if self.notify_all_users:
            return self.env['res.users'].search([])
        else:
            return self.user_ids | self.group_ids.mapped('users')

    @api.multi
    def button_send_all(self):
        # Send notification to all users listed in the announcement immediately
        self.ensure_one()
        users = self._get_users()
        users.sudo()._notify_channel(
            type_message=self.notify_type,
            message=self.popup_message,
            title=self.popup_title,
            sticky=self.is_always_show,
        )

    @api.multi
    def get_list_email_addr(self):
        # Return list of partner's from List users and list groups
        users = self._get_users()
        return ','.join(str(uid) for uid in users.mapped('partner_id').ids)

    @api.multi
    def button_send_mail_notification(self):
        '''
        This function opens a window to compose an email
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference(
                'web_announcement', 'email_template_announcement')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(
                'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'announcement',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_as_sent': True,
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
