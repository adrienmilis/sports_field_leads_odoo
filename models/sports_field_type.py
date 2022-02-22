from odoo import fields, models

class SportsFieldType(models.Model):

    _name = "sports_field_type"
    _description = "The type of the sports field (the original sport it's used for)"

    name = fields.Char(required=True)