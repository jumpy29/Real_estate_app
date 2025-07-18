from odoo import fields, models, api

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.properties', 
                                   "salesperson_id", string="Available Properties",
                                   domain=[('state', '=', 'new')])