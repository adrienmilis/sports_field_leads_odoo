from odoo import api, fields, models
import datetime

from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare

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

    for offer in self:
        if (offer.date_deadline and offer.create_date):
            offer.validity = (offer.date_deadline - offer.create_date).days
        else:
            offer.validity = None

class SportsFieldOffer(models.Model):

    _name = "sports_field_offer"
    _description = "An offer for a particular field with dates and price"
    _order = "monthly_price asc"

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

    _sql_constraints = [
        ('check_monthly_price', 'CHECK(monthly_price >= 0)',
            "Offer's monthly price should be greater or equal to 0."),
    ]

    # the offer monthly price cannot be higher than the field monthly price
    @api.constrains('monthly_price')
    def _check_monthly_price(self):
        
        for offer in self:
            if (float_compare(offer.monthly_price, offer.field_id.monthly_price, precision_digits=4) > 0):
                raise ValidationError("Offer's monthly price cannot be higher than the field's max price.")

    def action_offer_accepted(self):

        # once an order has been accepted, set the others to refused
        # --> self.field_id.offer_ids gives us all the offers
        for offer in self.field_id.offer_ids:
            if (offer != self):
                offer.status = 'refused'

        self.field_id.state = 'offer_accepted'
        for order in self:
            order.status = 'accepted'
            
            self.field_id.final_total_price = ((self.monthly_price * 12) / 365) * \
                    (self.to_date - self.from_date).days

    def action_offer_refused(self):

        for order in self:
            if (order.status == 'accepted'):
                self.field_id.final_total_price = None
            order.status = 'refused'