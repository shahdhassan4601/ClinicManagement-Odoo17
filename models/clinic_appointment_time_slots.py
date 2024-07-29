from odoo import api, fields, models



class ClinicAppointmentTimeSlots(models.Model):
    _name = 'clinic.appointment.time.slots'
    _description = 'Appointment Time Slots'

    name= fields.Char(string='Name', compute='_compute_name')
    doctor_id = fields.Many2one('res.users', string='Doctor')
    # appointment_id = fields.Many2one('clinic.appointment', string='Appointment')
    start_time = fields.Float('Start Time')
    end_time = fields.Float('End Time')
    count = fields.Integer("Number of Appointments", default=0)
    

    @api.depends('start_time','count')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.start_time} has {record.count}"