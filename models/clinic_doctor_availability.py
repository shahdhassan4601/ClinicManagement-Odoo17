from datetime import date, datetime, time, timedelta
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
    start_datetime = fields.Float(string='Start Time')
    end_datetime = fields.Float(string='End Time')
    
    @api.model
    def create(self, vals):

        res = super(DoctorAvailability, self).create(vals)
        
        hours = int(res.start_datetime)  # Get the integer part for hours
        minutes = int((res.start_datetime - hours) * 60)  # Calculate minutes

        current_date = datetime.combine(date.today(), time(hours, minutes, 0))
        utc_current_date = current_date.astimezone(pytz.UTC)     
        end_date = current_date + timedelta(days=30)
        
        diff = 1
        while current_date <= end_date:
            
            if current_date.weekday() == int(vals["week_day"]):
                
                x = (vals['end_datetime'] - vals['start_datetime']) * 3 
                while x:
                    self.env['clinic.appointment'].create({
                        'doctor_id': res.doctor_id.id,
                        'datetime': utc_current_date.strftime("%Y-%m-%d %H:%M:%S"),
                    })
                    utc_current_date += timedelta(hours=1/3)
                    x-=1
                # reset curent date time to 
            current_date = datetime.combine(date.today() + timedelta(days=diff), time(hours, minutes, 0))
            utc_current_date = current_date.astimezone(pytz.UTC)
            
            diff += 1
    
        return res
