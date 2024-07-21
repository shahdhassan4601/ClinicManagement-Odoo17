from odoo import api, fields, models


class ClinicProduct(models.Model):
    _name = 'clinic.medicine'
    
    
    # name = fields.Char(string='Medication Name')
    product_id = fields.Many2one('product.product', string='Product')
    # Add related field to store product type
    product_type = fields.Selection(related='product_id.detailed_type', string='Product Type', store=True)
    
    dose = fields.Integer(string='Dose')
    # dose_Unit = fields.Selection(string='Dose Unit', selection=[('mg', 'mg'), ('ml', 'ml'), ('mg/ml', 'mg/ml'),])
    frequency = fields.Char(string='Frequency (hours)')
    # frequency_Unit = fields.Char(string='Frequency Unit')
    notes = fields.Text(string='Notes')
    
    prescription_id = fields.Many2one('clinic.prescription', string='Prescription')
    treatment_id = fields.Many2one('clinic.treatment', string='Treatment')