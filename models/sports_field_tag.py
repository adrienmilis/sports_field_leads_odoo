from odoo import fields, models

class SportsFieldTag(models.Model):

    _name = "sports_field_tag"
    _description = "Tags are adjectives to describe the sports field"

    name = fields.Char(required=True)