import datetime

class TimeFunc:
	
	def today(self): return datetime.date.today()
	
	def this_year(self): return datetime.date.today().year
	
	def this_day(self): return datetime.date.today().day
	
	def this_month(self): return datetime.date.today().month
	
	def one_day(self): return datetime.timedelta(days=1)
	
	def one_week(self): return datetime.timedelta(days=7)
	
	def one_month(self): return datetime.timedelta(days=30)

	def two_weeks(self): return datetime.timedelta(days=14)
	
	def tree_weeks(self): return datetime.timedelta(days=21)
	
	def four_weeks(self): return datetime.timedelta(days=28)
	
	def quarter_year(self): return datetime.timedelta(days=int(365/4))
	
	def half_year(self): return datetime.timedelta(days=int(365/2))
	
	def one_year(self): return datetime.timedelta(days=365)
	
	def actual_day(self): return datetime.date.today().day
	
	def actual_month(self): return datetime.date.today().month
	
	def actual_year(self): return datetime.date.today().year
	
	def next_year(self): return self.this_year() + 1
	
	class Meta: abstract = True