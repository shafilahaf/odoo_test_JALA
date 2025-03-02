from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import requests
import json

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

    def action_fetch_logs(self):
        """ 
        Fetch logs from webhook.site based on the callback URL in the JALA webhook.
        """
        if not self.callback_url:
            raise UserError("No webhook callback URL found")

        webhook_site_token = self.callback_url.split('/')[-1]  # Get token from callback URL
        url = f"https://webhook.site/token/{webhook_site_token}/requests"
        headers = {"Accept": "application/json"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                requests_data = response.json()

                if isinstance(requests_data.get('data'), list):
                    for req in requests_data['data']:
                        if isinstance(req, dict) and 'uuid' in req:
                            # Check if the log exists already
                            existing_log = self.env['jala.trello.logs'].sudo().search([('log_id', '=', req.get('uuid', 'None'))], limit=1)
                            
                            if not existing_log:
                                self.env['jala.trello.logs'].sudo().create({
                                    'log_id': req.get('uuid', 'None'),
                                    'events_type': req.get('method', 'None'),
                                    'data': json.dumps(req, indent=4, ensure_ascii=False)
                                })
                    return{
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': _('Success'),
                            'message': _('Fetch Data is successful'),
                            'sticky': False
                        }
                    }
                else:
                    raise UserError("Invalid data format received")

            except json.JSONDecodeError:
                raise UserError("Failed to decode JSON response")

        raise UserError("Failed to fetch logs")
    
    def action_fetch_scheduler(self):
        """
        Scheduler for FETCH Logs
        """
        webhook = self.env['jala.trello.webhook'].search([('callback_url','!=','')])
        if webhook:
            webhook.action_fetch_logs()