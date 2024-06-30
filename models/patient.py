from odoo import api, fields, models


class Patient(models.Model):
    _inherit = 'res.partner'
    