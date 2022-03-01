from odoo import api, fields, models


@api.depends('offer_ids')
def _compute_offer_count(self):

    # self is actually all the records, not only our own
    for record in self:
        record.offer_count = len(record.offer_ids)

class SportsFieldType(models.Model):

    _name = "sports_field_type"
    _description = "The type of the sports field (the original sport it's used for)"
    _order = "sequence"

    name = fields.Char(required=True)
    sports_field_ids = fields.One2many(
        'sports_field',
        'sports_field_type_id',
        string="Sports fields"
    )
    sequence = fields.Integer(string="Sequence", default=1, help="Used to sort the fields in the view")
    offer_ids = fields.One2many('sports_field_offer', 'sports_field_type_id', string="Offer")
    offer_count = fields.Integer(compute=_compute_offer_count)

    _sql_constraints = [
        ('name_unique', 'unique(name)', "Sports field type name should be unique."),
    ]
