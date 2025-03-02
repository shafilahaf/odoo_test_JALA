from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class ProjectTaskInherit(models.Model):
    _inherit = 'project.task'

    trello_card_id = fields.Char(string="Trello Card ID", readonly=True)
    is_from_trello = fields.Boolean(string="From Trello", default=False, readonly=True)
    trello_start_date = fields.Date(string="Trello Start Date", readonly=True)
    trello_url = fields.Char(string="Trello URL", readonly=True)
    
    