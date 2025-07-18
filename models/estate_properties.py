from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from datetime import date, timedelta
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperties(models.Model):
    _name = 'estate.properties'  
    _description = 'Real estate app'
    _order = "id desc"

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
    default='new',
    readonly=True
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string='Buyer', copy = False)
    property_tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float(string='Best Offer', compute='_compute_best_price')
    

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price>0)', 'Expected prices must be greater than 0'),
        ('check_selling_price', 'CHECK(selling_price>0)', "Selling price must be greater than 0"),
        ('unique_name', 'UNIQUE(name)', "Property name already exists")
    ]



    # Python Constrains

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and record.selling_price<0.9*record.expected_price:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price")



    # Computed fields

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0

    

    # Onchange fields
                
    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else False


    # Property actions

    def set_property_sold(self):
        if self.state == 'cancelled':
            raise UserError("Cancelled properties cannot be sold.")
        
        for record in self:
            accepted_offer = record.offer_ids.filtered(lambda o : o.status=='accepted')
            if not accepted_offer:
                raise UserError("Property cannot be sold if no offer is accepted.")

        self.state = 'sold'
        return True
    
    def set_property_cancel(self):
        if self.state == 'sold':
            raise UserError("Sold properties cannot be cancelled.")
        
        for record in self:
            accepted_offer = record.offer_ids.filtered(lambda o : o.status=='accepted')
            if accepted_offer:
                raise UserError("Property cannot be sold when an offer is already accepted")

        self.state = 'cancelled'
        return True
    

    # CRUD logicv

    @api.ondelete(at_uninstall=False)
    def _check_property_before_delete(self):
        for record in self:
            if record.state not in ['cancelled', 'new']:
                raise ValidationError("Only 'new' or 'cancelled' properties can be deleted.")