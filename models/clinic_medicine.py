from odoo import api, fields, models


class ClinicProduct(models.Model):
    _name = 'clinic.medicine'
    
    
    # name = fields.Char(string='Medication Name')
    product_id = fields.Many2one('product.product', string='Product')
    # Add related field to store product type
    product_type = fields.Selection(related='product_id.detailed_type', string='Product Type', store=True)
    
    dose = fields.Integer(string='Dose')
    dose_Unit = fields.Selection(
        selection=[('mg', 'Milligrams'), ('ml', 'Milliliters'), ('unit', 'Units'),
        ('tsp', 'Teaspoons'), ('tbsp', 'Tablespoons'), ('caps', 'Capsules'), ('tablets', 'Tablets')],
        string='Dose Unit'
    )
    frequency = fields.Integer(string='Frequency')
    frequency_Unit = fields.Selection(
        selection=[('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('hour', 'Hour')],
        string='Frequency Unit')
    duration = fields.Integer(string='Duration')
    duration_Unit = fields.Selection(
        selection=[('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('hour', 'Hour'), ('year', 'Year')],
        string='Duration Unit')
    
    notes = fields.Text(string='Notes')
    
    prescription_id = fields.Many2one('clinic.prescription', string='Prescription')
    treatment_id = fields.Many2one('clinic.treatment', string='Treatment')