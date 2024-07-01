from datetime import datetime
from operator import gt
from odoo import api, fields, models


class ClinicDoctor(models.Model):
    _inherit = 'res.users'

    specialty = fields.Selection([
        ('general', 'General Practitioner'),
        ('cardiology', 'Cardiologist'),
        ('dermatology', 'Dermatologist'),
        ('neurology', 'Neurologist'),
        ('orthopedics', 'Orthopedist'),
        ('pediatrics', 'Pediatrician'),
        ('psychiatry', 'Psychiatrist'),
        ('radiology', 'Radiologist'),
        ('surgery', 'Surgeon'),
    ], string='Specialty')
    
    
    # Computed field
    availability = fields.Char(string='Availability', compute='_compute_availability')

    appointment_id = fields.One2many('clinic.appointment', 'doctor_id', string='Appointments')
    upcoming_appointments = fields.Integer(string='Upcoming Appointments', compute='_compute_upcoming_appointments')
        
    
    @api.depends('appointment_id')
    def _compute_availability(self):
        for doctor in self:
            appointments = self.env['clinic.appointment'].search([('doctor_id', '=', doctor.id), ('status', '=', 'confirmed')])
            if appointments:
                doctor.availability = 'Unavailable'
            else:
                doctor.availability = 'Available'
                
    @api.depends('appointment_id.datetime')
    def _compute_upcoming_appointments(self):
        for doctor in self:
            now = datetime.now()
            doctor.upcoming_appointments = len(doctor.appointment_id.filtered(lambda appointment: appointment.datetime and appointment.datetime > now))
            
