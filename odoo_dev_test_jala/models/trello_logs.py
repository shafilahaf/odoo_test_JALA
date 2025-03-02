from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import json

class TrelloLogs(models.Model):
    _name = 'jala.trello.logs'
    _description = 'Trello Logs'

    log_id = fields.Char(string="Logs ID")
    events_type = fields.Char(string="Type")
    data = fields.Text(string="Data", default='{}')
    actions = fields.Text(string="Action Data", compute="_compute_action", store=True)

    actions_type = fields.Char(string="Actions Type")
    translation_key = fields.Char(string="Actions Key")
    actions_before = fields.Char(string="Value Before")
    actions_after = fields.Char(string="Value After")
    tasks_id = fields.Many2one('project.task', string='Tasks')

    @api.depends('data')
    def _compute_action(self):
        """
        Get Action from Data JSON
        """
        for record in self:
            try:
                content_dict = json.loads(record.data)
                if "content" in content_dict:
                    content_data = json.loads(content_dict["content"])
                    record.actions = json.dumps(content_data.get("action", {}), indent=2)

                    actions_dict = json.loads(record.actions)
                    translation_key = actions_dict.get("display", {}).get("translationKey", "")
                    action_before = actions_dict.get("display", {}).get("entities", {}).get("listBefore", {}).get("text", "")
                    action_after = actions_dict.get("display", {}).get("entities", {}).get("listAfter", {}).get("text", "")

                    # Get Task ID
                    task_id = actions_dict.get("display", {}).get("entities", {}).get("card", {}).get("id", "")
                    task = self.env['project.task'].search([('trello_card_id','=',task_id)], limit=1)

                    record.tasks_id = task.id
                    record.translation_key = translation_key
                    record.actions_before = action_before
                    record.actions_after = action_after
                else:
                    record.actions = "{}"
                    record.translation_key = ""
                    record.tasks_id = False
                    record.actions_before = ""
                    record.actions_after = ""
            except json.JSONDecodeError:
                record.actions = "{}"
                record.translation_key = ""
                record.tasks_id = False
                record.actions_before = ""
                record.actions_after = ""

    