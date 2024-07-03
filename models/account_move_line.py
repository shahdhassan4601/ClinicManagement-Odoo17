from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _name = 'invoice.line'

    name = fields.Char(string='Name')
    price = fields.Float(string='Price')
    quantity = fields.Float(string='Quantity')
    total = fields.Float(string='Total', compute='_compute_total')
    invoice_id = fields.Many2one('account.move', string='Invoice')
    
    @api.depends('price', 'quantity')
    def _compute_total(self):
        for record in self:
            record.total = record.price * record.quantity