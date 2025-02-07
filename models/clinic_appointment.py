from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ClinicAppointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Appointment'

    # patient fields
    name = fields.Char(string='Name', readonly=True, default='New')
    patient_id = fields.Many2one('res.partner', string='Patient')
    
    # address computed field
    datetime = fields.Datetime('Date and Time')
    
    
    doctor_id = fields.Many2one('res.users', string='Doctor')
    doctor_speciality = fields.Selection(string='Doctor Speciality', related='doctor_id.specialty')
    doctor_availability = fields.Many2one('clinic.doctor.availability', string='Doctor Availability')


    duration = fields.Float('Duration (hh:mm)', compute='_compute_duration')
    
    start_time = fields.Datetime('Start Time')
    end_time = fields.Datetime('End Time')
    
    
    appointment_type = fields.Selection([
        ('consultation', 'Consultation'),
        ('emergency', 'Emergency'),
        ('checkup', 'Checkup'),
        ('surgery', 'Surgery'),
    ], string='Appointment Type')
    
    status = fields.Selection([
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('confirmed', 'Confirmed'),
    ], default='available')
    
    notes = fields.Text('Notes')
    
    treatment_id = fields.One2many('clinic.treatment','appointment_id', string='Treatment')
    
    medical_record_id = fields.One2many('clinic.medical.record','appointment_id', string='Medical History')
    
    log_id = fields.One2many('clinic.logs','appointment_id', string='Log')
    
    
    # overridden method create to add sequence
    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code('appointment.sequence')
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
    
    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        for record in self:
            if record.patient_id:
                record.status = 'pending'
    
    def patient_create_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Patient',
            'res_model': 'res.partner',  # Replace with your patient model name
            'view_mode': 'form',
            'view_id': self.env.ref('clinic.patient_views_form').id,  # Replace with your patient form view id
            'target': 'new',  # You can use 'new' to open in a new window
            'context': {'default_is_patient': 'True'}
        }
        
    def patient_view_action(self):
        patient_id = self.patient_id.id if self.patient_id else False
        if patient_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Patient Details',
                'res_model': 'res.partner', 
                'view_mode': 'form',
                'view_id': self.env.ref('clinic.patient_views_form').id,  
                'res_id': patient_id,  
                'target': 'new'
            }
        else:
            raise ValidationError("Please create patient first")
        
    def prescription_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Prescription',
            'res_model': 'clinic.prescription',
            'view_mode': 'form',
            'view_id': self.env.ref('clinic.prescription_form_view').id,
            'target': 'new',
            'context': {
                'default_appointment_id': self.id,
                'default_patient_id': self.patient_id.id,
                'default_doctor_id': self.doctor_id.id,
                'default_datetime': self.datetime
            },
        }
    def treatment_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Treatment',
            'res_model': 'clinic.treatment',
            'view_mode': 'form',
            'view_id': self.env.ref('clinic.treatment_form_view').id,
            'target': 'new',
            'context': {
                'default_appointment_id': self.id,
                'default_patient_id': self.patient_id.id,
                'default_doctor_id': self.doctor_id.id,
                'default_datetime': self.datetime,
                'default_id': self.treatment_id.id
            },
        }
    def treatment_edit_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Edit Treatment',
            'res_model': 'clinic.treatment',
            'res_id': self.treatment_id.id,
            'view_mode': 'form',
            'view_id': self.env.ref('clinic.treatment_form_view').id,
            'target': 'new',
            'context': {

            },
        }
        
    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for record in self:
            if record.start_time and record.end_time:
                # Calculate duration in hours
                duration_hours = (record.end_time - record.start_time).total_seconds() / 3600.0
                record.duration = duration_hours
            else:
                record.duration = 0.0
    
    def appointment_start_time(self):
        self.write({'status': 'confirmed'})
        self.start_time = fields.Datetime.now()
        
    def appointment_end_time(self):
        self.end_time = fields.Datetime.now()
        self._compute_duration()
        