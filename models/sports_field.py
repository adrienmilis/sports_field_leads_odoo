from odoo import fields, models
from datetime import date

# some attributes can impact the database schema
# some attributes can impact the view

def default_available_from(arg):

	today_date = date.today()
	if (today_date.month >= 9):
		return date(today_date.year + 1, 9, 1)
	else:
		return date(today_date.year, 9, 1)

def default_available_to(arg):

	today_date = date.today()
	if (today_date.month >= 9):
		return date(today_date.year + 2, 9, 1)
	else:
		return date(today_date.year + 1, 9, 1)


class SportsField(models.Model):

	_name = 'sports_field'
	_description = 'Properties of the potential sports fields to rent'

	name = fields.Char(size=50, required=True)
	description = fields.Text()
	postcode = fields.Char(size=10)
	yearly_days_off = fields.Integer()
	available_from = fields.Date(required=True, default=default_available_from)
	available_to = fields.Date(required=True, default = default_available_to)
	monthly_price = fields.Float(required=True)
	grass = fields.Boolean()
	# type_of_field = fields.Selection(
	# 	selection=[('hockey', 'Hockey'), ('football', 'Football'), ('rugby', 'Rugby'), ('other', 'Other')],
	# 	default='football',
	# 	help="Used to differentiate between different sports"
	# )
	booked_from = fields.Date(copy=False, readonly=True)
	booked_to = fields.Date(copy=False, readonly=True)
	final_total_price = fields.Float(copy=False, readonly=True)
	active = fields.Boolean(default=True)
	state = fields.Selection(
		selection=[('new', 'New'), ('offer_sent', 'Offer Sent'),
					('offer_accepted', 'Offer Accepted'), ('signed', 'Signed'),
					('canceled', 'Canceled')],
		default='new',
		required=True,
		copy=False
	)
	owner_id = fields.Many2one(
			'res.partner', string="Owner",
			help='The owner of the field',
			copy=False
	)
	# finder: defaults to the current user
	finder_id = fields.Many2one(
			'res.users', string='Finder',
			help="The club member that found the lead",
			default=lambda self: self.env.user
	)
	tag_ids = fields.Many2many('sports_field_tag', string="Tags")
