from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real estate property tag'

    name = fields.Char(required=True)
    