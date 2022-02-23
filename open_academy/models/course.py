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


class session(models.Model):
    _name = 'open_academy.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="duracion en dias")
    seats = fields.Integer(string="Cupos")     

    instructor_id = fields.Many2one('res.partner', string="Instructor")
    course_id = fields.Many2one('open_academy.course',
        ondelete='cascade', string="Course", required=True)
