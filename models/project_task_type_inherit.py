from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class ProjectTaskTypeInherit(models.Model):
    _inherit = 'project.task.type'

    trello_list_id = fields.Char(string="Trello List ID", readonly=True)
    is_from_trello = fields.Boolean(string="From Trello", default=False, readonly=True)
    trello_id_board = fields.Char(string="Trello Board ID", readonly=True)