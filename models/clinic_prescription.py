from odoo import api, fields, models


class ClinicPrescription(models.Model):
    _name = 'clinic.prescription'
    _description = 'Prescription'

    name = fields.Char(string='Name', readonly=True, default='New')
    doctor_id = fields.Many2one('res.users', string='Doctor')
    patient_id = fields.Many2one('res.partner', string='Patient')
    treatment_id = fields.Many2one('clinic.treatment', string='Treatment')
    appointment_id = fields.Many2one('clinic.appointment', string='Appointment')
    
    # medication details
    medication_name = fields.Char(string='Medication Name')
    dose = fields.Char(string='Dose')
    frequency = fields.Integer(string='Frequency (hours)')
    
    notes = fields.Text(string='Notes')
    
    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code('prescription.sequence')
        return super().create(vals)