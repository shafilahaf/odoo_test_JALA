from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class ProjectInherit(models.Model):
    _inherit = 'project.project'

    trello_board_id = fields.Char(string="Trello Board ID", readonly=True)
    is_from_trello = fields.Boolean(string="From Trello", default=False, readonly=True)
    trello_url = fields.Char(string="Trello URL", readonly=True)