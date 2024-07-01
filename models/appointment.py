from odoo import api, fields, models


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
    
