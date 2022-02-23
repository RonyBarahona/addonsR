# -*- coding: utf-8 -*-

from odoo import models, fields, api


class open_academy(models.Model):
    _name = 'open_academy.course'
    _description = 'course'

    name = fields.Char(string='Course')
    title = fields.Char(string='title')
    description = fields.Text(string='description')

    name = fields.Char(string="Title", required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('res.users',
        ondelete='set null', string="Responsible", index=True)
    """session_ids = fields.One2many(
        'openacademy.session', 'course_id', string="Sessions")"""
   


class session(models.Model):
    _name = 'open_academy.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="duracion en dias")
    seats = fields.Integer(string="Cupos") 
    active = fields.Boolean(default=True)    

    instructor_id = fields.Many2one('res.partner', string="Instructor",
        domain=['|', ('instructor', '=', True),
                     ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one('open_academy.course',
        ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }

    