# Copyright 2019 Dong Duc, DAO
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, SUPERUSER_ID


class ResUsers(models.Model):
    _inherit = "res.users"

    @classmethod
    def _login(cls, db, login, password):
        # Call notify function whenever user is log-ed
        user = super()._login(db=db, login=login, password=password)
        if user:
            with cls.pool.cursor() as cr:
                anm_env = api.Environment(cr, SUPERUSER_ID, {})['announcement']
                anm_env.check_is_announced(user)

        return user
