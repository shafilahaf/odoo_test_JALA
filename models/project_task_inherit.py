from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import requests

class ProjectTaskInherit(models.Model):
    _inherit = 'project.task'

    trello_card_id = fields.Char(string="Trello Card ID", readonly=True)
    is_from_trello = fields.Boolean(string="From Trello", default=False, readonly=True)
    trello_start_date = fields.Date(string="Trello Start Date", readonly=True)
    trello_url = fields.Char(string="Trello URL", readonly=True)
    
    @api.model
    def _update_trello_card(self, card_id, new_name):
        """ 
        Update trello from Odoo.

        Curent : Only changes name.
        """
        trello_setup = self.env['jala.trello.setup'].search([('is_active', '=', True)])

        trello_api_key = trello_setup.trello_api_key
        trello_token = trello_setup.trello_token

        if not trello_api_key or not trello_token:
            raise UserError(_("Trello API Key or Token is missing!"))

        url = f"https://api.trello.com/1/cards/{card_id}"
        params = {
            'key': trello_api_key,
            'token': trello_token,
            'name': new_name
        }
        response = requests.put(url, params=params)

        if response.status_code != 200:
            raise UserError(_("Failed to update Trello card: %s") % response.text)

    def write(self, vals):
        """ Override name in trello """
        for task in self:
            if 'name' in vals and task.trello_card_id:
                self._update_trello_card(task.trello_card_id, vals['name'])
        return super(ProjectTaskInherit, self).write(vals)