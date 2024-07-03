from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ClinicAppointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Appointment'

    # patient fields
    name = fields.Char('Appointment', default='New', readonly=True)
    # appointments_id = fields.Char('Appointment', default='New', readonly=True)
    patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    
    # address computed field
    address = fields.Char('Address', compute='_compute_address')
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
    
    medical_record_id = fields.One2many('clinic.medical.record','appointment_id', string='Medical Record')
    
    log_id = fields.One2many('clinic.logs','appointment_id', string='Log')
    
    
    # overridden method create to add sequence
    @api.model
    def create(self, vals):
        res = super(ClinicAppointment, self).create(vals)
        if res.name == 'New':
            res.name = self.env['ir.sequence'].next_by_code('appointment.sequence')
        return res
    
    # # computed fields
    # @api.depends('appointments_id')
    # def _compute_name(self):
    #     for record in self:
    #         record.name = record.appointments_id
    
    
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
            
        
        
    @api.model
    def create(self, vals):
        res = super(ClinicAppointment, self).create(vals)
        res.log_id.create({
            'patient_id': res.patient_id.id,
            'appointment_id': res.id,
            'doctor_id': res.doctor_id.id,
            'create_uid': res.create_uid,
            'entry_datetime': res.datetime,
            'notes': res.notes
        })
        return res
    