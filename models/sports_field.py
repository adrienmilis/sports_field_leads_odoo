from odoo import api, fields, models, exceptions
from datetime import date

# some attributes can impact the database schema
# some attributes can impact the view

def default_available_from(arg):

	today_date = date.today()
	if (today_date.month >= 9):
		return date(today_date.year + 1, 9, 1)
	else:
		return date(today_date.year, 9, 1)

# the dependency triggers a recomputation when one of the fields is changed
@api.depends('available_to', 'available_from')
def _compute_total_price(self):

	for record in self:
		if (self.available_from is not None and self.available_to is not None):
			daily_price = (self.monthly_price * 12) / 365
			self.total_price = daily_price * (self.available_to - self.available_from).days
		else:
			self.total_price = None

@api.depends('offer_ids.monthly_price')
def _compute_best_monthly_price(self):

	if (self.offer_ids):
		self.best_monthly_price = min(self.offer_ids.mapped('monthly_price'))
	else:
		self.best_monthly_price = 0


def default_available_to(arg):

	today_date = date.today()
	if (today_date.month >= 9):
		return date(today_date.year + 2, 9, 1)
	else:
		return date(today_date.year + 1, 9, 1)

# modifies one record at a time in the form view when grass is checked

class SportsField(models.Model):

	_name = 'sports_field'
	_description = 'Properties of the potential sports fields to rent'

	name = fields.Char(size=50, required=True)
	description = fields.Text()
	postcode = fields.Char(size=10)
	yearly_days_off = fields.Integer(default=0)
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
	total_price = fields.Float(compute=_compute_total_price)
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
	best_monthly_price = fields.Float(compute=_compute_best_monthly_price)
	_sql_constraints = [
		('check_monthly_price', 'CHECK(monthly_price >= 0)',
			'Monthly price should be greater or equal to 0.'),
	]

	### relations

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
	# one field can have many offers
	offer_ids = fields.One2many('sports_field_offer', 'field_id', string="Offers")

	@api.onchange('grass')
	def _onchange_grass(self):
		self.yearly_days_off = 10

	# when we make an offer, the monthly price cannot be higher than 100%
	# of the field's monthly price

	def action_sold(self):
		
		for record in self:
			if (record.state != 'canceled'):
				record.state = 'signed'
			else:
				raise exceptions.UserError('Canceled fields cannot be set as signed.')

	def action_cancel(self):
		
		for record in self:
			if (record.state != 'signed'):
				record.state = 'canceled'
			else:
				raise exceptions.UserError('Signed fields cannot be set as canceled.')