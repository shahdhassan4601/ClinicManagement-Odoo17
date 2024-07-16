from datetime import date, datetime, time, timedelta, timezone
from xml.dom import ValidationErr
import pytz

from odoo import api, fields, models


class DoctorAvailability(models.Model):
    _name = 'clinic.doctor.availability'
    _description = 'Doctor Availability'

    doctor_id = fields.Many2one('res.users', string='Doctor')
    week_day = fields.Selection([
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday')
    ])
    start_datetime = fields.Float(string='Start Time', widget="float_time")
    end_datetime = fields.Float(string='End Time', widget="float_time")
    
    
    
    def _create_appointments(self):
        current_date = datetime.now()
        current_date = current_date.astimezone(pytz.timezone('UTC')).replace(tzinfo=None)
        end_date = current_date + timedelta(weeks=4)
        
        while current_date <= end_date:
            if current_date.weekday() == int(self.week_day):
                end_time = self.end_datetime
                start_time = self.start_datetime
                while start_time <= end_time:
                    appointment_date = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=start_time)
                    cairo_tz = pytz.timezone('Africa/Cairo')
                    appointment_date = cairo_tz.localize(appointment_date, is_dst=None)
                    appointment_date = appointment_date.astimezone(pytz.timezone('UTC')).replace(tzinfo=None)
                    
                    self.env['clinic.appointment'].create({
                        'doctor_id': self.doctor_id.id,
                        'datetime': appointment_date
                    })
                    start_time += 0.25
            current_date += timedelta(days=1)

    @api.model
    def create(self, vals):
        res = super(DoctorAvailability, self).create(vals)
        res._create_appointments()
        return res

    def write(self, vals):
        res = super(DoctorAvailability, self).write(vals)
        for record in self:
            # Calculate the specific dates based on the week_day
            current_date = datetime.now()
            current_date = current_date.astimezone(pytz.timezone('UTC')).replace(tzinfo=None)
            end_date = current_date + timedelta(weeks=4)
            
            affected_dates = []
            while current_date <= end_date:
                if current_date.weekday() == int(record.week_day):
                    affected_dates.append(current_date.date())
                current_date += timedelta(days=1)
            
            # Delete old appointments on the affected dates
            for date in affected_dates:
                start_of_day = datetime.combine(date, datetime.min.time())
                end_of_day = datetime.combine(date, datetime.max.time())
                old_appointments = self.env['clinic.appointment'].search([
                    ('doctor_id', '=', record.doctor_id.id),
                    ('datetime', '>=', start_of_day),
                    ('datetime', '<=', end_of_day)
                ])
                old_appointments.unlink()
            
            # Create new appointments
            record._create_appointments()
        return res
