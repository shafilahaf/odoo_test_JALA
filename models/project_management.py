from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class ProjectMgt(models.Model):
    _name = 'project.management'
    _rec_name = 'project_name'
    _description = 'Project Management'

    project_name = fields.Char(string="Nama Proyek", required=True)
    description = fields.Text(string="Deskripsi")
    start_date = fields.Date(string="Tanggal Mulai", required=True)
    end_date = fields.Date(string="Tanggal Selesai", required=True)
    state = fields.Selection([('aktif', 'Aktif'), ('selesai', 'Selesai'), ('ditangguhkan', 'Ditangguhkan')], string="Status", default='aktif')
    
    # Shafilah - Add new field
    duration = fields.Integer(string="Durasi", compute="_compute_duration", store=True)
    project_owner = fields.Many2one('res.users', string="Pemilik Proyek", required=True)

    @api.onchange('project_owner')
    def _onchange_project_owner(self):
        """
        Validation project owner
        """
        if self.project_owner and not self.project_owner.email:
            self.project_owner = False
            return {
                'warning': {
                    'title': _("Peringatan"),
                    'message': _("Pemilik proyek harus memiliki email. Silakan pilih user yang memiliki email."),
                }
            }

    def write(self, vals):
        """
        Send an email to project owner when the state project is changed.
        """
        for rec in self:
            old_state = rec.state
            new_state = vals.get('state', old_state)

            # Check if the state is changed
            res = super(ProjectMgt, self).write(vals)

            if old_state != new_state:
                mail_template_notif = self.env.ref('odoo_test_JALA.jala_project_mgt_notif_status_mail_template')
                if mail_template_notif:
                    mail_template_notif.send_mail(rec.id, force_send=True)

            return res

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        """
        Compute the duration of the project in days, based on the start_date and end_date
        """
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.duration = (rec.end_date - rec.start_date).days
                rec.duration = max(rec.duration, 0)
            else:
                rec.duration = 0

    