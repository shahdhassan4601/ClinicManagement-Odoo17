from datetime import datetime, timedelta
from operator import gt
from odoo import api, fields, models


class ClinicDoctor(models.Model):
    _inherit = 'res.users'

    specialty = fields.Selection([
        ('general', 'General'),
        ('cardiology', 'Cardiology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('gynaecology', 'Gynaecology'),
        ('dermatology', 'Dermatology'),
        ('urology', 'Urology'),
        ('neurology', 'Neurology'),
        ('oncology', 'Oncology'),
        ('obstetrics', 'Obstetrics'),
        ('emergency', 'Emergency'),
        ('surgery', 'Surgery'),
        ('dentistry', 'Dentistry'),
        ('gastroenterology', 'Gastroenterology'),
    ], string='Specialty')
    
    is_doctor = fields.Boolean('Is Doctor')
    
    # Computed field
    doctor_availability = fields.One2many('clinic.doctor.availability', 'doctor_id')
    
    appointment_id = fields.One2many('clinic.appointment', 'doctor_id', string='Appointments')
    # patient_id = fields.
    available_appointments = fields.One2many('clinic.appointment', 'doctor_id', compute='_compute_available_appointments')
    reversed_appointments = fields.One2many('clinic.appointment', 'doctor_id', compute='_compute_reserved_appointments')
        
    
    # @api.depends('appointment_id')
    # def _compute_availability(self):
    #     for record in self:
            
                
    @api.depends('appointment_id')
    def _compute_available_appointments(self):
        for record in self:
            record.available_appointments = record.appointment_id.filtered(
                lambda a: a.status == 'available' and a.datetime and a.datetime > fields.Datetime.now()
            )
    @api.depends('appointment_id')
    def _compute_reserved_appointments(self):
        for record in self:
            record.reversed_appointments = record.appointment_id.filtered(
                lambda a: a.status == 'pending' and a.datetime and a.datetime > fields.Datetime.now()
            )

            
