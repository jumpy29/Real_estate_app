from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type'
    _order = 'sequence, name'
    
    sequence = fields.Integer('Sequence', default=1, help = 'Used to order property types')
    name = fields.Char(string='Name', required=True)
    property_ids = fields.One2many('estate.properties', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(string=' Offers', compute='_compute_offer_count')



    # Computed Fields

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
