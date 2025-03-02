from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import requests

class TrelloWebhook(models.Model):
    _name = 'jala.trello.webhook'
    _description = 'Trello Webhook'

    project_id = fields.Many2one('project.project', string="Project", required=True)
    id_webhook = fields.Char(string="Webhook ID", readonly=True)
    description = fields.Char(string="Webhook Description", readonly=True)
    callback_url = fields.Char(string="Callback URL")
    is_active = fields.Boolean(string="Active", readonly=True)

    def create_webhook(self):
        """
        Create webhook in Trello"""
        trello_setup = self.env['jala.trello.setup'].search([], limit=1)
        url = "https://api.trello.com/" + str(1) +"/tokens/" + trello_setup.trello_token + "/webhooks/"
        
        if not trello_setup:
            raise UserError(_("Trello setup is not configured"))
        
        if not self.callback_url:
            raise UserError(_("Callback URL is required. Please visit https://webhook.site/ to get a callback URL. Make sure to copy the URL with https:// prefix."))
        
        query = {
            'key': trello_setup.trello_api_key,
            'callbackURL': self.callback_url,
            'idModel': self.project_id.trello_board_id,
            'description': 'Webhook for ' + self.project_id.name
        }
        response = requests.post(url, params=query)
        if response.status_code == 200:
            response_json = response.json()
            self.id_webhook = response_json['id']
            self.description = response_json['description']
            self.is_active = response_json['active']
        else:
            raise UserError(_("Failed to create webhook"))
        
    def delete_webhook(self):
        """
        Delete webhook from Trello"""
        trello_setup = self.env['jala.trello.setup'].search([], limit=1)
        url = "https://api.trello.com/1/webhooks/" + self.id_webhook
        query = {
            'key': trello_setup.trello_api_key,
            'token': trello_setup.trello_token
        }
        response = requests.delete(url, params=query)
        if response.status_code != 200:
            raise UserError(_("Failed to delete webhook"))
        self.id_webhook = False
        self.description = False
        self.is_active = False