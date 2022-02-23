from odoo import fields, models

class SportsFieldOffer(models.Model):

    _name = "sports_field_offer"
    _description = "An offer for a particular field with dates and price"

    monthly_price = fields.Float(required=True)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    from_date = fields.Date(required=True)
    to_date = fields.Date(required=True)
    # many offers can be made by one finder (club member)
    finder_id = fields.Many2one('res.users', required=True)
    # there can be many offers for one field
    field_id = fields.Many2one('sports_field', required=True)