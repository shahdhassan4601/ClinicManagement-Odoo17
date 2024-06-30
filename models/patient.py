from odoo import api, fields, models


class Patient(models.Model):
    _inherit = 'res.partner'
    
    # Base fields
    # Unique ID
    patient_id = fields.Char('Patient ID', default='New', readonly=True)
    date_of_birth = fields.Date(string='Date of Birth')
    
    # insurance info fields
    is_insurance = fields.Boolean('Insurance')
    insurance_company = fields.Char('Insurance Company')
    policy_number = fields.Integer('Policy Number')
    expiry_date = fields.Date('Expiry Date', default= fields.Date.today())
    coverage_details = fields.Selection(
        selection=[('full_coverage', 'Full Coverage'), ('partial_coverage', 'Partial Coverage'), ('no_coverage', 'No Coverage')],
        string="Coverage Details",
        default="full_coverage"
    )
    
    # emergency contact
    emergency_contact_name = fields.Char('Emergency Contact Name')
    emergency_contact_number = fields.Char('Emergency Contact Number')
    
    
    
    
    
    

    