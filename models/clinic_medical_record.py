from odoo import api, fields, models


class ClinicMedicalRecord(models.Model):
    _name = 'clinic.medical.record'
    _description = 'Medical Record'

    patient_id = fields.Many2one('res.partner', string='Patient')
    doctor_id = fields.Many2one('res.users', string='Doctor')
    appointment_id = fields.Many2one('clinic.appointment', string='Appointment')
    appointment_datetime = fields.Datetime(string='Appointment Date', related='appointment_id.datetime', store=True)
    treatment_ref = fields.One2many('clinic.treatment', 'medical_record_id',string='Treatment')
    prescription_id= fields.One2many('clinic.prescription','medical_record_id', string='Prescription')
    
    is_uploadable_files = fields.Boolean(string='Uploadable Files')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    notes = fields.Text(string='Notes')
    
    