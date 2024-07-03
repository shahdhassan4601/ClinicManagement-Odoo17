from odoo import api, fields, models


class ClinicLogs(models.Model):
    _name = 'clinic.logs'
    _description = 'Logs'

    patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    appointment_id = fields.Many2one('clinic.appointment', string='Appointment')
    # create_uid = fields.Many2one('',string='Created By', related='appointment_id.create_uid')
    entry_datetime = fields.Datetime(string='Entry Datetime', required=True)
    notes = fields.Text(string='Notes')

    