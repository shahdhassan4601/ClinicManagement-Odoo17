from odoo import api, fields, models


class ClinicTreatment(models.Model):
    _name = 'clinic.treatment'
    _description = 'Treatment'
    
    patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    doctor_id = fields.Many2one('res.users', string='Doctor', required=True)
    appointment_id = fields.Many2one('clinic.appointment', string='Appointment', required=True)
    
    # treatment fields
    treatment_diagnosis = fields.Text('Diagnosis')
    treatment_prescription = fields.One2many('clinic.prescription', 'treatment_id', string='Prescription')
    treatment_procedure = fields.Text('Procedure')
    
    treatment_details = fields.Text('Treatment Details', compute='_compute_treatment_details')
    
    # medical record fields
    # medical_record = fields.One2many('clinic.medical.record', 'treatment_id', string='Medical Records')
    
    notes = fields.Text('Notes')
    
    @api.depends('treatment_diagnosis', 'treatment_prescription', 'treatment_procedure')
    def _compute_treatment_details(self):
        for record in self:
            record.treatment_details = f"Diagnosis: {record.treatment_diagnosis}\nPrescription: {record.treatment_prescription}\nProcedure: {record.treatment_procedure}"
                
    
    @api.onchange('appointment_id')
    def _onchange_appointment_id(self):
        if self.appointment_id:
            self.patient_id = self.appointment_id.patient_id
            self.doctor_id = self.appointment_id.doctor_id
