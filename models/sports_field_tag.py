from odoo import fields, models

class SportsFieldTag(models.Model):

    _name = "sports_field_tag"
    _description = "Tags are adjectives to describe the sports field"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', "Tag name should be unique."),
    ]