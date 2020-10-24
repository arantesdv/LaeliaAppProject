import io
from reportlab.lib.pagesizes import letter, A4, A5
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (Flowable, Paragraph,
                                BaseDocTemplate, Spacer, SimpleDocTemplate)


########################################################################


class LineFlowable(Flowable):
	"""
	Line flowable --- draws a line in a flowable
	http://two.pairlist.net/pipermail/reportlab-users/2005-February/003695.html
	"""
	# ----------------------------------------------------------------------
	def __init__(self,  width, height=0):
		Flowable.__init__(self)
		self.width = width
		self.height = height

	# ----------------------------------------------------------------------
	def __repr__(self):
		return f"Line(w={self.width})"
	# ----------------------------------------------------------------------
	def draw(self):
		"""
		draw the line
		"""
		self.canv.line(0, self.height, self.width, self.height)



class BoxyLine(Flowable):
	"""
	Draw a box + line + text

	-----------------------------------------
	| foobar |
	---------

	"""
	
	# ----------------------------------------------------------------------
	def __init__(self, x=0, y=-15, width=40, height=15, text=""):
		Flowable.__init__(self)
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.styles = getSampleStyleSheet()
	
	# ----------------------------------------------------------------------
	def coord(self, x, y, unit=1):
		"""
		http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
		Helper class to help position flowables in Canvas objects
		"""
		x, y = x * unit, self.height - y * unit
		return x, y
	
	# ----------------------------------------------------------------------
	def draw(self):
		"""
		Draw the shape, text, etc
		"""
		self.canv.rect(self.x, self.y, self.width, self.height)
		self.canv.line(self.x, 0, 500, 0)
		self.canv.line(0, self.x, self.y, self.y)

		
		p = Paragraph(self.text, style=self.styles["Normal"])
		p.wrapOn(self.canv, self.width, self.height)
		p.drawOn(self.canv, *self.coord(self.x + 2, 10, mm))
