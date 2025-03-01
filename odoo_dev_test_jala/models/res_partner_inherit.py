from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    trello_member_id = fields.Char(string="Trello Member ID")
    is_from_trello = fields.Boolean(string="From Trello", default=False)
    trello_url = fields.Char(string="Trello URL")