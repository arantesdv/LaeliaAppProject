from io import BytesIO
from reportlab.lib.pagesizes import letter, A5, A4

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER
from reportlab.lib.units import inch, mm
from reportlab.platypus import (Flowable,
                                Paragraph,
                                SimpleDocTemplate,
                                Spacer,
                                ListFlowable, ListItem)
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.html import format_html
from Laelia.pdf.flowables import LineFlowable, BoxyLine
from Laelia.apps.care.models import Visit
from Laelia.apps.base.models import Relation
from . functions import Styles


########################################################################

class PdfCreator:
	def __init__(self, pagesize, relation_id):
		self.pdf_buffer = BytesIO()
		if pagesize == 'A4': self.pagesize = A4
		elif pagesize == 'A5': self.pagesize = A5
		self.width = self.pagesize[0]
		self.height = self.pagesize[1]
		self.styles = Styles.compile()
		self.relation = get_object_or_404(Relation, pk=relation_id)



	
	def _header_footer(self, canvas, doc):
		# Save the state of our canvas so we can draw on it
		relation = self.relation
		canvas.saveState()
		styles = Styles.compile()
		footer = Paragraph(f'{relation.professional.full_name}', styles['footer'])
		w, h = footer.wrap(doc.width + doc.leftMargin, doc.bottomMargin)
		footer.drawOn(canvas, 0, doc.bottomMargin - h)
		doc.bottomMargin -= h
		address = Paragraph(f'{relation.professional.full_address}', styles['small-right'])
		w, h = address.wrap(doc.width + doc.leftMargin, doc.bottomMargin)
		address.drawOn(canvas, 0, doc.bottomMargin - h)
		doc.bottomMargin -= h
		number = Paragraph(f'{relation.professional.main_phone}', styles['small-right'])
		w, h = number.wrap(doc.width + doc.leftMargin, doc.bottomMargin)
		number.drawOn(canvas, 0, doc.bottomMargin - h)
		# page number
		canvas.setFont('Times-Roman', 10)
		styles['Normal'].alignment = 1
		page_number_text = Paragraph("%d" % (doc.page), styles['Normal'])
		w, h = page_number_text.wrap(doc.width, doc.bottomMargin)
		page_number_text.drawOn(canvas, 0, doc.bottomMargin - h)
		# Release the canvas
		canvas.restoreState()
	#
		
		
	def create_visit(self, context={}):
		doc = SimpleDocTemplate(
				self.pdf_buffer,
				pagesize=self.pagesize,
				width=self.pagesize[0],
				height=self.pagesize[1],
				leftMargin=self.width * 0.05,
				topMargin=self.height * 0.05,
				bottomMargin=self.height * 0.05,
				rightMargin=self.width * 0.05,
			)
		filename = f'Visita {self.relation.patient} x {self.relation.professional} {context["date"]}'
		canvas.Canvas(filename, self.pagesize)
		flowables = []
		flowables.append(Paragraph(f'{context["patient"]}', self.styles['h1T']))
		flowables.append(Spacer(0, 7))
		flowables.append(LineFlowable(doc.width))
		flowables.append(Spacer(0, 3))
		flowables.append(Paragraph(f'{self.relation.local_site_name} / {self.relation.local_site_full_address}', self.styles['small']))
		flowables.append(Paragraph(f'Visita dia {context["date"]}', self.styles['h2T']))
		if context['introduction']: flowables.append(Paragraph(f'{context["introduction"]}', self.styles['body']))
		if context['section_1']: flowables.append(Paragraph(f'{context["section_1"]}', self.styles['body']))
		if context['section_2']: flowables.append(Paragraph(f'{context["section_2"]}', self.styles['body']))
		if context['section_3']: flowables.append(Paragraph(f'{context["section_3"]}', self.styles['body']))
		if context['plan']:
			content = context['plan']
			items = f'{content}'.splitlines(keepends=False)
			flowables.append(Paragraph(f"PLANO TERAPÊUTICO DIA {context['date']}", self.styles['h2T']))
			plan = list()
			for item in items:
				plan.append(ListItem(Paragraph(f'{item}', self.styles["Normal"])))
			flowables.append(ListFlowable(plan))
	
	
		doc.build(
			flowables,
			onFirstPage=self._header_footer,
			onLaterPages=self._header_footer,
		)
		# Get the value of the BytesIO buffer and write it to the response.
		pdf = self.pdf_buffer.getvalue()
		self.pdf_buffer.close()
		return pdf
	
	def create_visit_plan(self, relation_id, context={}):
		relation = get_object_or_404(Relation, pk=relation_id)
		doc = SimpleDocTemplate(
			self.pdf_buffer,
			pagesize=self.pagesize,
			width=self.pagesize[0],
			height=self.pagesize[1],
			leftMargin=self.width * 0.05,
			topMargin=self.height * 0.05,
			bottomMargin=self.height * 0.05,
			rightMargin=self.width * 0.05,
		)
		filename = f'Plano Terapêutico {relation.patient} x {relation.professional} {context["date"]}'
		canvas.Canvas(filename, self.pagesize)
		flowables = []
		flowables.append(Paragraph(f'{context["patient"]}', self.styles['h1T']))
		flowables.append(Spacer(0, 7))
		flowables.append(LineFlowable(doc.width))
		flowables.append(Spacer(0, 3))
		flowables.append(
			Paragraph(f'{relation.local_site_name} / {relation.local_site_full_address}', self.styles['small']))
		flowables.append(Paragraph(f'Plano Terapêutico {context["date"]}', self.styles['h2T']))
		if context['plan']:
			content = context['plan']
			items = f'{content}'.splitlines(keepends=False)
			flowables.append(Paragraph(f"PLANO TERAPÊUTICO DIA {context['date']}", self.styles['h2T']))
			plan = list()
			for item in items:
				plan.append(ListItem(Paragraph(f'{item}', self.styles["Normal"])))
			flowables.append(ListFlowable(plan))
		
		doc.build(
			flowables,
			onFirstPage=self._header_footer,
			onLaterPages=self._header_footer,
		)
		# Get the value of the BytesIO buffer and write it to the response.
		pdf = self.pdf_buffer.getvalue()
		self.pdf_buffer.close()
		return pdf
	
	def create_medical_licence(self, context={}):
		doc = SimpleDocTemplate(
			self.pdf_buffer,
			pagesize=self.pagesize,
			width=self.pagesize[0],
			height=self.pagesize[1],
			leftMargin=self.width * 0.05,
			topMargin=self.height * 0.05,
			bottomMargin=self.height * 0.05,
			rightMargin=self.width * 0.05,
		)
		filename = f'Visita {self.relation.patient} x {self.relation.professional} {context["date"]}'
		canvas.Canvas(filename, self.pagesize)
		flowables = []
		flowables.append(Paragraph(f'{context["patient"]}', self.styles['h1T']))
		flowables.append(Spacer(0, 7))
		flowables.append(LineFlowable(doc.width))
		flowables.append(Spacer(0, 3))
		flowables.append(Paragraph(f'{self.relation.local_site_name} / {self.relation.local_site_full_address}',
		                           self.styles['small']))
		flowables.append(Spacer(0, 7))
		flowables.append(Paragraph('LICENÇA MÉDICA', self.styles["Heading2"]))
		if context['introduction']: flowables.append(Paragraph(f'{context["introduction"]}', self.styles['body']))
		if context['section_1']: flowables.append(Paragraph(f'{context["section_1"]}', self.styles['body']))
		if context['section_2']: flowables.append(Paragraph(f'{context["section_2"]}', self.styles['body']))
		if context['section_3']: flowables.append(Paragraph(f'{context["section_3"]}', self.styles['body']))
		if context['finalization']: flowables.append(Paragraph(f'{context["finalization"]}', self.styles['body']))
		doc.build(
			flowables,
			onFirstPage=self._header_footer,
			onLaterPages=self._header_footer,
		)
		# Get the value of the BytesIO buffer and write it to the response.
		pdf = self.pdf_buffer.getvalue()
		self.pdf_buffer.close()
		return pdf
