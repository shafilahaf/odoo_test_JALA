from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import requests

class TrelloSetup(models.Model):
    _name = 'jala.trello.setup'
    _rec_name = 'name'
    _description = 'Trello Setup'

    name = fields.Char(string="Name", required=True)
    trello_api_key = fields.Char(string="Trello API Key", required=True)
    trello_api_secret = fields.Char(string="Trello API Secret", required=True)
    trello_token = fields.Char(string="Trello Token", required=True)
    is_active = fields.Boolean(string="Active", default=True)

    is_sync_board = fields.Boolean(string="Sync Board", default=False)
    is_sync_list = fields.Boolean(string="Sync List", default=False)
    is_sync_card = fields.Boolean(string="Sync Card", default=False)
    is_sync_member = fields.Boolean(string="Sync Member", default=False)

    def check_trello_connection(self):
        """
        Check Trello connection
        """
        self.ensure_one()
        url = f'https://api.trello.com/1/members/me'
        params = {
            'key': self.trello_api_key,
            'token': self.trello_token
        }

        if not self.trello_api_key or not self.trello_token:
            raise UserError(_("Trello API Key and Token must be filled."))
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return{
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': _('Connection to Trello is successful'),
                    'sticky': False
                }
            }
        else:
            raise UserError(f'Failed to connect to Trello. Error: {response.text}')

    def action_syncronize(self):
        """
        Syncronize data from Trello to Odoo
        """
        self.ensure_one()
        if self.is_sync_board:
            self.sync_board()
        if self.is_sync_list:
            self.sync_list()
        if self.is_sync_card:
            self.sync_card()
        if self.is_sync_member:
            self.sync_member()

        if self.is_sync_board or self.is_sync_list or self.is_sync_card or self.is_sync_member:
            return{
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': _('Syncronize data from Trello to Odoo is successful'),
                    'sticky': False
                }
            }
        else:
            raise UserError(_("Please select at least one option to syncronize data."))

    def sync_board(self):
        """
        Syncronize board data from Trello to Odoo and create new board in project.project model
        """
        self.ensure_one()
        url = f'https://api.trello.com/1/members/me/boards'
        params = {
            'key': self.trello_api_key,
            'token': self.trello_token
        }

        if not self.trello_api_key or not self.trello_token:
            raise UserError(_("Trello API Key and Token must be filled."))
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            boards = response.json()
            for board in boards:
                project = self.env['project.project'].search([('trello_board_id', '=', board.get('id'))])
                if not project:
                    self.env['project.project'].create({
                        'name': board.get('name'),
                        'description': board.get('desc'),
                        'trello_board_id': board.get('id'),
                        'trello_url': board.get('url'),
                        'is_from_trello': True
                    })
                else:
                    project.write({
                        'name': board.get('name'),
                        'description': board.get('desc'),
                        'trello_board_id': board.get('id'),
                        'trello_url': board.get('url'),
                        'is_from_trello': True
                    })
        else:
            raise UserError(f'Failed to sync board from Trello. Error: {response.text}')

    def sync_list(self):
        """
        Syncronize list data from Trello to Odoo and create new list in project.task.type model
        """
        self.ensure_one()
        project = self.env['project.project'].search([('is_from_trello', '=', True)])
        if not project:
            raise UserError(_("Please sync board first before sync list."))
        
        for project in project:
            url = f'https://api.trello.com/1/boards/{project.trello_board_id}/lists'
            params = {
                'key': self.trello_api_key,
                'token': self.trello_token
            }

            response = requests.get(url, params=params)
            if response.status_code == 200:
                lists = response.json()
                for list in lists:
                    task_type = self.env['project.task.type'].search([('trello_list_id', '=', list.get('id'))])
                    if not task_type:
                        self.env['project.task.type'].create({
                            'name': list.get('name'),
                            'trello_list_id': list.get('id'),
                            'is_from_trello': True,
                            'trello_id_board': list.get('idBoard'),
                            'project_ids': [(6, 0, project.ids)]
                        })
                    else:
                        task_type.write({
                            'name': list.get('name'),
                            'trello_list_id': list.get('id'),
                            'is_from_trello': True,
                            'trello_id_board': list.get('idBoard'),
                            'project_ids': [(6, 0, project.ids)]
                        })
            else:
                raise UserError(f'Failed to sync list from Trello. Error: {response.text}')
            
    def sync_card(self):
        """
        Syncronize card data from Trello to Odoo and create new card in project.task model
        """
        self.ensure_one()
        task_type = self.env['project.task.type'].search([('is_from_trello', '=', True)])
        if not task_type:
            raise UserError(_("Please sync list first before sync card."))
        
        for task_type in task_type:
            url = f'https://api.trello.com/1/lists/{task_type.trello_list_id}/cards'
            params = {
                'key': self.trello_api_key,
                'token': self.trello_token
            }

            response = requests.get(url, params=params)
            if response.status_code == 200:
                cards = response.json()
                for card in cards:
                    task = self.env['project.task'].search([('trello_card_id', '=', card.get('id'))])
                    project = self.env['project.project'].search([('trello_board_id', '=', task_type.trello_id_board)])
                    # Get members
                    members = card.get('idMembers')
                    member_ids = []
                    for member in members:
                        partner = self.env['res.partner'].search([('trello_member_id', '=', member)])
                        if partner:
                            users = self.env['res.users'].search([('partner_id', '=', partner.id)])
                            if users:
                                member_ids.append(users.id)
                    if not task:
                        self.env['project.task'].create({
                            'name': card.get('name'),
                            'description': card.get('desc'),
                            'trello_card_id': card.get('id'),
                            'is_from_trello': True,
                            'project_id': project.id,
                            'stage_id': task_type.id,
                            'date_deadline': card.get('due'),
                            'trello_start_date': card.get('start'),
                            'trello_url': card.get('url'),
                            'user_ids': [(6, 0, member_ids)],
                        })
                    else:
                        task.write({
                            'name': card.get('name'),
                            'description': card.get('desc'),
                            'trello_card_id': card.get('id'),
                            'is_from_trello': True,
                            'project_id': project.id,
                            'stage_id': task_type.id,
                            'date_deadline': card.get('due'),
                            'trello_start_date': card.get('start'),
                            'trello_url': card.get('url'),
                            'user_ids': [(6, 0, member_ids)],
                        })
            else:
                raise UserError(f'Failed to sync card from Trello. Error: {response.text}')
            
    def sync_member(self):
        """
        Syncronize member data from Trello to Odoo and create new member in res.users and res.partner model
        """
        self.ensure_one()
        url = f'https://api.trello.com/1/members/me'
        params = {
            'key': self.trello_api_key,
            'token': self.trello_token
        }

        if not self.trello_api_key or not self.trello_token:
            raise UserError(_("Trello API Key and Token must be filled."))
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            member = response.json()
            partner = self.env['res.partner'].search([('trello_member_id', '=', member.get('id'))])
            if not partner:
                self.env['res.partner'].create({
                    'name': member.get('fullName'),
                    'email': member.get('email'),
                    'trello_member_id': member.get('id'),
                    'is_from_trello': True,
                    'trello_url': member.get('url')
                })
            else:
                partner.write({
                    'name': member.get('fullName'),
                    'email': member.get('email'),
                    'trello_member_id': member.get('id'),
                    'is_from_trello': True,
                    'trello_url': member.get('url')
                })

            # Create user
            user = self.env['res.users'].search([('partner_id', '=', partner.id)])
            if not user:
                self.env['res.users'].create({
                    'name': member.get('fullName'),
                    'login': member.get('username'),
                    'partner_id': partner.id,
                    'password': "1234",
                })
            else:
                user.write({
                    'name': member.get('fullName'),
                    'login': member.get('username'),
                    'partner_id': partner.id,
                    'password': "1234",
                })
        else:
            raise UserError(f'Failed to sync member from Trello. Error: {response.text}')