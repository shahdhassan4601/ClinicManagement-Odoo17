from odoo import api, fields, models


class ClinicTreatment(models.Model):
    _name = 'clinic.treatment'
    _description = 'Treatment'
    
    patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    doctor_id = fields.Many2one('res.users', string='Doctor', required=True)
    appointment_id = fields.Many2one('clinic.appointment', string='Appointment', required=True)
    
    treatment_diagnosis = fields.Text('Diagnosis')
    treatment_prescription = fields.Text('Prescription')
    treatment_procedure = fields.Text('Procedure')
    
    notes = fields.Text('Notes')