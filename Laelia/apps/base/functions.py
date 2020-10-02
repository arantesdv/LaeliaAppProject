import datetime
from django.utils.translation import gettext_lazy as _

def funcTime(x):
	if isinstance(x, str):
		if x == 'today': return datetime.datetime.today()
		elif x == 'this year': return datetime.date.today().year
		elif x == 'this day': return datetime.date.today().day
		elif x == 'this month': return datetime.date.today().month
	elif isinstance(x, int):
		return datetime.timedelta(days=x)
	else: return None
	

def processVolumeTo_ml(unit):
	if not unit: raise ValueError(_('You need input a unit.'))
	if unit == ('ml' or 'mL'): value = 1
	elif unit == ('cl' or 'cL'): value = 10
	elif unit == ('dl' or 'dL'): value = 100
	elif unit == ('l' or 'L'): value = 1000
	return value, 'ml'

def processWeightTo_mg(unit):
	if not unit: raise ValueError(_('You need input a unit.'))
	normVal = None
	if unit == ('mg'): normVal = 1
	elif unit == ('mcg' or 'μg'): normVal = 0.001
	elif unit == ('cg'): normVal = 10
	elif unit == ('dg'): normVal = 100
	elif unit == ('g' or 'G'): normVal = 1000
	return normVal, 'mg'