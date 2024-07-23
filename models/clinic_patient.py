from datetime import date
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ClinicPatient(models.Model):
    _inherit = 'res.partner'
    
    # Base fields
    # Unique ID
    patient_id = fields.Char('Patient ID', default='New', readonly=True)
    # override the phone field to make it required
    phone = fields.Char(string='Phone', required=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', required=True)
    
    is_patient = fields.Boolean(string='Is a Patient', default=False)

    
    # address computed field
    address = fields.Char('Address', compute='_compute_address')
    
    # appointment fields
    appointment_id = fields.One2many('clinic.appointment', 'patient_id', string='Appointments')
    upcoming_appointments = fields.One2many('clinic.appointment', 'patient_id', string='Upcoming Appointments', 
                                            compute='_compute_upcoming_appointments')
        
    # emergency contact
    emergency_contact_name = fields.Char('Emergency Contact Name')
    emergency_contact_number = fields.Char('Emergency Contact Number')
    
    # insurance info fields
    is_insurance = fields.Boolean('Insurance')
    insurance_company = fields.Char('Insurance Company')
    policy_number = fields.Char('Policy Number')
    expiry_date = fields.Date('Expiry Date', default= fields.Date.today())
    coverage_details = fields.Selection(
        selection=[('full_coverage', 'Full Coverage'), ('partial_coverage', 'Partial Coverage'), ('no_coverage', 'No Coverage')],
        string="Coverage Details",
        default="full_coverage"
    )
    
    
    # medical record fields
    medical_record = fields.One2many('clinic.medical.record', 'patient_id', string='Medical Records')   
    
    # prescription field
    prescription = fields.One2many('clinic.prescription', 'patient_id', string='Prescriptions')
    
    # overridden method create to add sequence
    @api.model
    def create(self, vals):
        # check before creating a new patient if the phone number already exists or not if it is exists create a wizrd of all the possible patients in the system and ask the user to choose one and if not create a new one
        res = super(ClinicPatient, self).create(vals)
        if res.patient_id == 'New':
            res.patient_id = self.env['ir.sequence'].next_by_code('patient.sequence')
        return res
    
    
    # computed fields
    @api.depends('street', 'street2', 'city', 'state_id', 'zip', 'country_id')
    def _compute_address(self):
        for record in self:
            address_parts = [
                record.street or '',
                record.street2 or '',
                record.city or '',
                record.state_id.name if record.state_id else '',
                record.zip or '',
                record.country_id.name if record.country_id else '',
            ]
            # Join non-empty parts with commas
            record.address = ', '.join(filter(None, address_parts))
            
            
    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                birth_date = fields.Date.from_string(record.date_of_birth)
                record.age = (date.today() - birth_date).days // 365
            else:
                record.age = 0
                
    
    @api.depends('appointment_id.end_time')
    def _compute_upcoming_appointments(self):
        for record in self:
            record.upcoming_appointments = record.appointment_id.filtered(
                lambda a: a.status in ['pending','confirmed'] and a.datetime and a.datetime > fields.Datetime.now() and ( (not a.end_time) or a.end_time > fields.Datetime.now()) 
            )
    
    # field constraints 
    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for record in self:
            if record.date_of_birth and record.date_of_birth > fields.Date.today():
                raise ValidationError("Date of Birth cannot be in the future.")


    @api.constrains('expiry_date')
    def _check_expiry_date(self):
        for record in self:
            if record.expiry_date and record.expiry_date < fields.Date.today():
                raise ValidationError("Expiry Date must be in the future.")

    # contrain on the phone number to begin with 01 and have 11 digits
    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone and not record.phone.startswith('01') or len(record.phone) != 11:
                raise ValidationError("Phone Number must start with 01 and have 11 digits.")