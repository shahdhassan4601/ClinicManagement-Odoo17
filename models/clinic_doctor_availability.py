from datetime import date, datetime, time, timedelta, timezone
from xml.dom import ValidationErr
import pytz

from odoo import api, fields, models


class DoctorAvailability(models.Model):
    _name = 'clinic.doctor.availability'
    _description = 'Doctor Availability'
    _rec_name = 'week_day'

    doctor_id = fields.Many2one('res.users', string='Doctor')
    week_day = fields.Selection([
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday')
    ])
    start_datetime = fields.Float(string='Start Time', widget="float_time")
    end_datetime = fields.Float(string='End Time', widget="float_time")
    

    