# Code Profilling
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)
class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        res = super(StockPickingInherit, self).create(vals)

        self._query_test1()
        self._query_test2()

        return res
    
    def _query_test1(self):
        self.env.cr.execute("select pg_sleep(1*10)")

    def _query_test2(self):
        self.env.cr.execute("select pg_sleep(1*20)")