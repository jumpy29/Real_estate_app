from odoo import models, fields
from datetime import date, timedelta

class EstateProperties(models.Model):
    _name = 'estate.properties'  #name of table
    _description = 'Real estate app'

    #table fields
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    availability_from = fields.Date(default=date.today()+timedelta(days=90), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], 
    required=True, 
    copy=False,
    default='new'
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string='Buyer', copy = False)
    property_tag_ids = fields.Many2many('estate.property.tag', string='Tags')