from odoo import api, fields, models
import datetime

# populates the field
@api.depends('create_date', 'validity')
def _compute_date_deadline(self):

    for offer in self:
        if (offer.validity and offer.create_date):
            offer.date_deadline = offer.create_date + datetime.timedelta(days=offer.validity)
        else:
            offer.date_deadline = None


# populates dependencies
# called when saving the record
def _inverse_date_deadline(self):

    print("\n========== TEST =========\n")
    for offer in self:
        if (offer.date_deadline and offer.create_date):
            offer.validity = (offer.date_deadline - offer.create_date).days
        else:
            offer.validity = None

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
    create_date = fields.Date(default=datetime.date.today())
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute=_compute_date_deadline, inverse=_inverse_date_deadline)

    ### relations
    # many offers can be made by one finder (club member)
    finder_id = fields.Many2one('res.users', required=True)
    # there can be many offers for one field
    field_id = fields.Many2one('sports_field', required=True)