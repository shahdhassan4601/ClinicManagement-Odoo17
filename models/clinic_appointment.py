from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ClinicAppointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Appointment'

    # Base fields
    patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    datetime = fields.Datetime('Date and Time', required=True)
    doctor_id = fields.Many2one('res.users', string='Doctor', required=True)
    appointment_type = fields.Selection([
        ('consultation', 'Consultation'),
        ('emergency', 'Emergency'),
        ('checkup', 'Checkup'),
        ('surgery', 'Surgery'),
    ], string='Appointment Type', required=True)
    
    status = fields.Selection([
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('confirmed', 'Confirmed'),
    ], default='pending', required=True)
    
    notes = fields.Text('Notes')
    
    treatment_id = fields.One2many('clinic.treatment','appointment_id', string='Treatment')
    
    # constraints
    @api.constrains('datetime', 'doctor_id')
    def _check_conflict(self):
        for record in self:
            conflicting_appointments = self.search([
                ('doctor_id', '=', record.doctor_id.id),
                ('datetime', '=', record.datetime),
                ('id', '!=', record.id)
            ])
            if conflicting_appointments:
                raise ValidationError('The doctor is already booked for this time slot. Please choose another time.')
    
