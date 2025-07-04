from odoo import api, models, fields
from odoo.exceptions import UserError
from datetime import timedelta, date

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = 'Real estate property offer'

    price = fields.Float(required=True)
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False, readonly=True)
    partner_id = fields.Many2one('res.partner', required=True, string='Buyer')
    property_id = fields.Many2one('estate.properties', required=True, string='Property')
    
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)


    _sql_constraints = [
        ('check_price', 'CHECK(price>0)', 'Offer price must be greater than 0')
    ]


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



    # Offer actions

    def offer_accept(self):
        #checking if property already sold
        if self.property_id.buyer_id:
            raise UserError("Cannot accept more than one offers for a property")
        
        if self.date_deadline and self.date_deadline < date.today():
            raise UserError("Deadline for offer has passed.")

        self.property_id.state = 'offer_accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.status = 'accepted'

        #refuse all other offers on the same property
        for other_offer in self.property_id.offer_ids:
            if other_offer != self:
                other_offer.status = 'refused'

        return True
    
    def offer_refuse(self):
        if (self.status=='accepted'):
            raise UserError("Cannot refuse offer that is already accepted")
        
        self.status = 'refused'

        return True