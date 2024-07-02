from odoo import api, fields, models


class ClinicMedicalRecord(models.Model):
    _name = 'clinic.medical.record'
    _description = 'Medical Record'

    date = fields.Date(string='Date')
    patient_id = fields.Many2one('res.partner', string='Patient')
    doctor_id = fields.Many2one('res.users', string='Doctor')
    appointment_id = fields.Many2one('clinic.appointment', string='Appointment')
    treatment_ref = fields.Many2many('clinic.treatment', string='Treatment')
    is_uploadable_files = fields.Boolean(string='Uploadable Files')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    notes = fields.Text(string='Notes')
    
    