import requests
import json
from odoo import http
from odoo.http import request, Response

class TrelloWebhookFetcher(http.Controller):

    @http.route('/jala/trello/fetch_logs', type='http', auth='public', methods=['GET'])
    def fetch_webhook_data(self):
        """ 
        Get All request from webhook.site based on callback in JALA webhook trello.
        """

        webhook = request.env['jala.trello.webhook'].sudo().search([], limit=1)
        if not webhook or not webhook.callback_url:
            return Response("No webhook callback URL found", status=400)

        webhook_site_token = webhook.callback_url.split('/')[-1]  # Get token from callback url
        url = f"https://webhook.site/token/{webhook_site_token}/requests"
        headers = {"Accept": "application/json"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                requests_data = response.json()

                if isinstance(requests_data.get('data'), list):
                    for req in requests_data['data']:
                        if isinstance(req, dict) and 'uuid' in req:
                            # Check exist data
                            existing_log = request.env['jala.trello.logs'].sudo().search([('log_id', '=', req.get('uuid', 'None'))], limit=1)
                            
                            if not existing_log:
                                request.env['jala.trello.logs'].sudo().create({
                                    'log_id': req.get('uuid', 'None'),
                                    'events_type': req.get('method', 'None'),
                                    'data': json.dumps(req, indent=4, ensure_ascii=False)
                                })
                    return Response(f"{len(requests_data['data'])} logs fetched", status=200)
                else:
                    return Response("Invalid data format received", status=400)

            except json.JSONDecodeError:
                return Response("Failed to decode JSON response", status=500)

        return Response("Failed to fetch logs", status=500)
