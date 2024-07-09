from odoo import api, fields, models


class ClinicLogs(models.Model):
    _name = 'clinic.logs'
    _description = 'Logs'

    patient_id = fields.Many2one('res.partner', string='Patient')
    doctor_id = fields.Many2one('res.users', string='Doctor')
    appointment_id = fields.Many2one('clinic.appointment', string='Appointment')
    entry_datetime = fields.Datetime(string='Entry Datetime')
    notes = fields.Text(string='Notes')

    