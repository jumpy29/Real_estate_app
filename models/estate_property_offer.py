from odoo import api, models, fields
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = 'Real estate property offer'

    price = fields.Float(required=True)
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True, string='Buyer')
    property_id = fields.Many2one('estate.properties', required=True, string='Property')
    
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)



    #Computed Fields

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days
