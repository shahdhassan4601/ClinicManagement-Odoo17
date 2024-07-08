import calendar
from datetime import date, timedelta
from odoo import api, fields, models


class DoctorAvailability(models.Model):
    _name = 'clinic.doctor.availability'
    _description = 'Doctor Availability'

    doctor_id = fields.Many2one('res.users', string='Doctor')
    week_day = fields.Selection([
        ('6', 'Friday'),
        ('7', 'Saturday'),
        ('1', 'Sunday'),
        ('2', 'Monday'),
        ('3', 'Tuesday'),
        ('4', 'Wednesday'),
        ('5', 'Thursday')
    ])
    start_datetime = fields.Float(string='Start Time')
    end_datetime = fields.Float(string='End Time')
    
    @api.model
    def create(self, vals):
        res = super(DoctorAvailability, self).create(vals)
        current_date = date.today()
        end_date = current_date + timedelta(days=90)
        dates_list = []
        while current_date <= end_date:
            if current_date.weekday() == self.week_day:
                dates_list.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
    
        for date_str in dates_list:
            print(date_str)
        return res
