from odoo import api, fields, models


class ClinicPrescription(models.Model):
    _name = 'clinic.prescription'
    _description = 'Prescription'

    name = fields.Char(string='Name', readonly=True, default='New')
    
    
    doctor_id = fields.Many2one('res.users', string='Doctor', readonly=True)
    patient_id = fields.Many2one('res.partner', string='Patient', readonly=True)
    treatment_id = fields.Many2one('clinic.treatment', string='Treatment')
    appointment_id = fields.Many2one('clinic.appointment', string='Appointment', readonly=True)
    datetime = fields.Datetime(string='Date', related='appointment_id.datetime')
    

    medicines = fields.One2many('clinic.medicine','prescription_id', string='Medicines')
    
    medical_record_id = fields.Many2one('clinic.medical.record', string='Medical Record')
    
    notes = fields.Text(string='Notes')
    
    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code('prescription.sequence')
        return super().create(vals)