from datetime import date, datetime, time, timedelta, timezone
from xml.dom import ValidationErr
import pytz

from odoo import api, fields, models


class DoctorAvailability(models.Model):
    _name = 'clinic.doctor.availability'
    _description = 'Doctor Availability'

    name = fields.Char(string='Name', compute='_compute_name')
    doctor_id = fields.Many2one('res.users', string='Doctor')
    doctor_speciality = fields.Selection(string='Doctor Speciality', related='doctor_id.specialty', store=True, readonly=False)
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
    

    @api.depends('week_day',"start_datetime","end_datetime")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.week_day} ({record.start_datetime} - {record.end_datetime})"
            
    # override create method to create appointment time slots in the clinic appointment time slots model to create slots every 15 minutes
    @api.model
    def create(self, vals):
        res=super().create(vals)
        res.create_time_slots()
        return res

    def create_time_slots(self):
        for availability in self:
            start_time = availability.start_datetime
            end_time = availability.end_datetime

            while start_time < end_time:
                slot_end_time = start_time + 0.25
                if slot_end_time > end_time:
                    break
                
                self.env['clinic.appointment.time.slots'].create({
                'doctor_id': self.doctor_id.id,
                'availability_id': self.id,
                'start_time': start_time,
                'end_time': end_time
                })
                
                start_time = slot_end_time
        