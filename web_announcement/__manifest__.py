# Copyright 2019 Dong Duc, DAO
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Web Announcement',
    'summary': """Create and send announcements to users""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Dong Duc, DAO (blakice12@gmail.com)',
    'website': 'https://github.com/OCA/web',
    'depends': [
        'mail',
        'web_notify',
    ],
    'data': [
        # Data
        'data/announcement_data.xml',
        'data/email_template_announcement.xml',

        # Views
        'views/announcement_view.xml',

        # Security
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
