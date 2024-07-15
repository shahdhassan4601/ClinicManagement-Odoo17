from odoo import api, fields, models


class ClinicProduct(models.Model):
    _name = 'clinic.medicine'
    
    
    name = fields.Char(string='Medication Name')
    dose = fields.Char(string='Dose')
    frequency = fields.Integer(string='Frequency (hours)')
    notes = fields.Text(string='Notes')
    
    prescription_id = fields.Many2one('clinic.prescription', string='Prescription')