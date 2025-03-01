from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class TrelloLogs(models.Model):
    _name = 'jala.trello.logs'
    _description = 'Trello Logs'

    events_type = fields.Char(string="Type")
    data = fields.Text(string="Data")