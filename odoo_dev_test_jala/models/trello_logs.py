from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import json

class TrelloLogs(models.Model):
    _name = 'jala.trello.logs'
    _description = 'Trello Logs'

    log_id = fields.Char(string="Logs ID")
    events_type = fields.Char(string="Type")
    data = fields.Text(string="Data", default='{}')
    actions = fields.Text(string="Action Data", store=True)

    actions_type = fields.Char(string="Actions Type")
    translation_key = fields.Char(string="Actions Key")
    actions_before = fields.Char(string="Value Before")
    actions_after = fields.Char(string="Value After")
    tasks_id = fields.Many2one('project.task', string='Tasks')

    is_from_webhook = fields.Boolean(string="Webhook")

    @api.model
    def create(self, vals):
        """
        When create will update stage tasks.
        Current : only update stage based on action_move_card_from_list_to_list translation key
        """
        record = super(TrelloLogs, self).create(vals)
        
        if record.translation_key == 'action_move_card_from_list_to_list' and record.tasks_id:
            task = record.tasks_id

            if task.stage_id.name != record.actions_after:
                task_stages = self.env['project.task.type'].search([('name','=',record.actions_after)])
                task.write({'stage_id': task_stages.id})

        return record