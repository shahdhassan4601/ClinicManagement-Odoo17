from odoo import api, fields, models


class ClinicPrescription(models.Model):
    _name = 'clinic.prescription'
    _description = 'Prescription'

    name = fields.Char(string='Name', readonly=True, default='New')
    datetime = fields.Datetime(string='Date', default=fields.Datetime.now())
    
    
    doctor_id = fields.Many2one('res.users', string='Doctor')
    patient_id = fields.Many2one('res.partner', string='Patient')
    treatment_id = fields.Many2one('clinic.treatment', string='Treatment')
    appointment_id = fields.Many2one('clinic.appointment', string='Appointment')

    medicines = fields.One2many('clinic.medicine','prescription_id', string='Medicines')
    
    notes = fields.Text(string='Notes')
    
    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code('prescription.sequence')
        return super().create(vals)