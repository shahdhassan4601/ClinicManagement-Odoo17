from odoo import api, fields, models


class ClinicProduct(models.Model):
    _name = 'clinic.medicine'
    
    
    # name = fields.Char(string='Medication Name')
    product_id = fields.Many2one('product.product', string='Product')
    dose = fields.Integer(string='Dose')
    frequency = fields.Char(string='Frequency (hours)')
    notes = fields.Text(string='Notes')
    
    prescription_id = fields.Many2one('clinic.prescription', string='Prescription')
    treatment_id = fields.Many2one('clinic.treatment', string='Treatment')