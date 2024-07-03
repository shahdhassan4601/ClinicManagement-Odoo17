from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    name = fields.Char(string='Name', default='New', readonly=True)
    patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    appointment_id = fields.Many2one('clinic.appointment', string='Appointment')
    treatment_id = fields.Many2many('clinic.treatment', string='Treatment')
    invoice_lines = fields.One2many('invoice.line', 'invoice_id', string='Invoice Lines')
    
    
    
    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        if res.name == 'New':
            res.name = self.env['ir.sequence'].next_by_code('invoice.sequence')
        return res