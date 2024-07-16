from odoo import api, fields, models


class ClinicTreatment(models.Model):
    _name = 'clinic.treatment'
    _description = 'Treatment'
    
    
    name = fields.Char(string='Name', readonly=True, default='New')
    
    patient_id = fields.Many2one('res.partner', string='Patient', required=True, readonly=True)
    doctor_id = fields.Many2one('res.users', string='Doctor', required=True, readonly=True)
    appointment_id = fields.Many2one('clinic.appointment', string='Appointment', required=True, readonly=True)
    datetime = fields.Datetime(string='Date', related='appointment_id.datetime', readonly=True)
    
    # treatment fields
    treatment_diagnosis = fields.Text('Diagnosis')
    prescripted_medication = fields.Many2one('clinic.prescription', string='Prescripted Medication')
    medicines = fields.One2many('clinic.medicine',  'treatment_id' ,string='Medicines')
    products = fields.Many2many('product.product', string='Procedures')
    
    procedure = fields.Text('Procedure')
    
    notes = fields.Text('Notes')
    
    
    # treatment_details = fields.Text('Treatment Details', compute='_compute_treatment_details')
    
    # medical record fields
    # medical_record = fields.One2many('clinic.medical.record', 'treatment_id', string='Medical Records')
    
    
    # @api.depends('treatment_diagnosis', 'treatment_prescription', 'treatment_procedure')
    # def _compute_treatment_details(self):
    #     for record in self:
    #         record.treatment_details = f"Diagnosis: {record.treatment_diagnosis}\nPrescription: {record.treatment_prescription}\nProcedure: {record.treatment_procedure}"
                
    
    # @api.onchange('appointment_id')
    # def _onchange_appointment_id(self):
    #     if self.appointment_id:
    #         self.patient_id = self.appointment_id.patient_id
    #         self.doctor_id = self.appointment_id.doctor_id

    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code('treatment.sequence')
        
        return super().create(vals)
    
            
            
    def prescription_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Prescription',
            'res_model': 'clinic.prescription',
            'view_mode': 'form',
            'view_id': self.env.ref('clinic.prescription_form_view').id,
            'target': 'new',
            'context': {
                'default_appointment_id': self.appointment_id.id,
                'default_patient_id': self.patient_id.id,
                'default_doctor_id': self.doctor_id.id,
                'default_datetime': self.datetime
            },
        }