from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ClinicAppointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Appointment'

    # patient fields
    name = fields.Char(string='Name', readonly=True, default='New')
    patient_id = fields.Many2one('res.partner', string='Patient')
    
    # address computed field
    address = fields.Char('Address', compute='_compute_address')
    datetime = fields.Datetime('Date and Time')
    
    
    doctor_id = fields.Many2one('res.users', string='Doctor')
    doctor_speciality = fields.Selection([
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
    ], string='Doctor Speciality', related='doctor_id.specialty')
    doctor_availability = fields.Many2one('clinic.doctor.availability', string='Doctor Availability')
    # doctor_availability_from = fields.Float('Doctor Availability From', related='doctor_availability.start_datetime')
    # doctor_availability_to = fields.Float('Doctor Availability To', related='doctor_availability.end_datetime')
    
    
    
    duration = fields.Float('Duration (hh:mm)', default=(1/3))
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
    
    medical_record_id = fields.One2many('clinic.medical.record','appointment_id', string='Medical Record')
    
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
    def action_reserve(self):
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
            'context': self.env.context
        }