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
    medicines = fields.One2many('clinic.medicine',  'treatment_id' ,string='Medicines', domain=[('product_type', '=', 'product')])
    services = fields.One2many('clinic.medicine',  'treatment_id' ,string='Procedures', domain=[('product_type', '=', 'service')])
    
    medical_record_id = fields.Many2one('clinic.medical.record', string='Medical Record')

    
    
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
        treatment = super().create(vals)
        self.env['clinic.medical.record'].create({
            'patient_id': treatment.patient_id.id,
            'doctor_id': treatment.doctor_id.id,
            'appointment_id': treatment.appointment_id.id,
            'appointment_datetime': treatment.datetime,
            'treatment_ref': [(4, treatment.id)],
            # 'prescription_details': treatment.prescription_details,
        })
        return treatment
    
    def write(self, vals):
        res = super().write(vals)
        if 'patient_id' in vals or 'doctor_id' in vals:
            medical_record = self.env['medical.record'].search([('treatment_ref', 'in', [self.id])], limit=1)
            if medical_record:
                medical_record.write({
                   'patient_id': self.patient_id.id,
                    'doctor_id': self.doctor_id.id,
                    'appointment_id': self.appointment_id.id,
                    'appointment_datetime': self.datetime,
                    'treatment_ref': [(4, self.id)],
                })
        return res
            
            
    def prescription_action(self):
        self.ensure_one()        
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
                'default_datetime': self.datetime,
            },
        }
            