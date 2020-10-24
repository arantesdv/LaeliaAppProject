from io import BytesIO
from reportlab.lib.pagesizes import A5, A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER
from reportlab.lib.units import inch, mm
from reportlab.platypus import (Paragraph,
                                SimpleDocTemplate,
                                Spacer,
                                ListFlowable, ListItem)
from django.shortcuts import get_object_or_404, get_list_or_404
from reportlab.pdfgen import canvas
########################################################################
from .elements import LineFlowable


########################################################################


class PdfBuilder(object):
	'''PDF builder object'''
	def __init__(self, pagesize, relation, context):
		'''
		PDF builder init method responsible to get bites, canvas and doc objects and set page size and styles.
		Pagesize can be set to "A5" or "A4" as strings.
		'''
		self.buffer = BytesIO()
		self.styles = getSampleStyleSheet()
		if pagesize == 'A4': self.pagesize = A4
		elif pagesize == 'A5': self.pagesize = A5
		self.width = self.pagesize[0]
		self.height = self.pagesize[1]
		self.relation = relation
		self.type = context['type']
		self.patient = context['patient']
		self.professional = context['professional']
		self.title = context['main_title']
		self.introduction = context['introduction']
		self.section_1 = context['section_1']
		self.section_2 = context['section_2']
		self.section_3 = context['section_3']
		self.finalization = context['finalization']
		
		if self.type == 'Visit': self.create_visit()
		
	
	def _header_footer(self, canvas, doc):
		# Save the state of our canvas so we can draw on it
		canvas.saveState()
		styles = getSampleStyleSheet()
		styles.add(ParagraphStyle('footer', parent=styles['Heading3'], alignment=2, fontSize=10, leading=10, textColor='grey'))
		styles.add(ParagraphStyle('small-right', parent=styles['Normal'], alignment=2, fontSize=8, leading=8, textColor='grey'))

		# Footer
		footer = Paragraph(f'{self.relation.professional.sponsor}', styles['footer'])
		w, h = footer.wrap(doc.width + doc.leftMargin, doc.bottomMargin)
		footer.drawOn(canvas, 0, doc.bottomMargin - h)
		doc.bottomMargin -= h
		address = Paragraph(f'{self.relation.professional.sponsor.full_address}', styles['small-right'])
		w, h = address.wrap(doc.width + doc.leftMargin, doc.bottomMargin)
		address.drawOn(canvas, 0, doc.bottomMargin - h)
		doc.bottomMargin -= h
		number = Paragraph(f'{self.relation.professional.sponsor.main_phone}', styles['small-right'])
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


	def h1(self): return ParagraphStyle('h1', parent=self.styles['Heading1'], fontSize=18, leading=10)
	def h2(self): return ParagraphStyle('h2', parent=self.styles['Heading2'], fontSize=12, leading=12)
	def h2s(self): return ParagraphStyle('h2s', parent=self.styles['Heading2'], fontSize=8, leading=10, textColor='grey')
	def h3(self): return ParagraphStyle('h3', parent=self.styles['Heading3'], fontSize=8, leading=10)
	def h4(self): return ParagraphStyle('h4', parent=self.styles['Heading4'], fontSize=10, leading=12)
	def h6c(self): return ParagraphStyle('h6c', parent=self.styles['Heading6'], alignment=1, fontSize=8, leading=12)
	def regular(self): return ParagraphStyle('regular', parent=self.styles['Normal'], fontSize=12, leading=14)
	def small(self): return ParagraphStyle('small', parent=self.styles['Normal'], fontSize=10, leading=12)
	def body(self): return ParagraphStyle('body', parent=self.styles['BodyText'], fontSize=11, leading=12)
	def right(self): return ParagraphStyle('right', parent=self.styles['Normal'], alignment=2)
	def centered(self): return ParagraphStyle('centered', parent=self.styles['Normal'], alignment=TA_CENTER)
	def signature(self): return ParagraphStyle('signature', parent=self.styles['Normal'], alignment=1, fontSize=10, leading=10, bold=1)
	def small_centered(self): return ParagraphStyle('small-centered', parent=self.styles['Normal'], alignment=1, fontSize=8, leading=8,textColor='grey')
	def footer(self): return ParagraphStyle('footer', parent=self.styles['Heading3'], alignment=2, fontSize=10, leading=8,textColor='grey')
	def small_right(self): return ParagraphStyle('small-right', parent=self.styles['Normal'], alignment=2, fontSize=8, leading=8,
		                          textColor='grey')

	
	def create_visit(self):
		buffer = self.buffer
		doc = SimpleDocTemplate(
			buffer,
			width=self.width,
			height=self.height,
			rightMargin=self.width * 0.05,
			leftMargin=self.width * 0.05,
			topMargin=self.height * 0.05,
			bottomMargin=self.height * 0.1,
			pagesize=self.pagesize
		)
		elements = list()
		elements.append(Paragraph("RECEITA DE CONTROLE ESPECIAL", self.h6c()))
		elements.append(Paragraph(f'Médico: {self.professional}', self.h4()))
		elements.append(Paragraph(f'Paciente: {self.patient}', self.h4()))
		doc.build(
			elements,
			onFirstPage=self._header_footer,
			onLaterPages=self._header_footer,
			)
		# Get the value of the BytesIO buffer and write it to the response.
		pdf = buffer.getvalue()
		buffer.close()
		return pdf


######################################################################## PAST


class PdfCreator(object):
	'''PDF constructor class'''
	
	def __init__(self, pagesize):
		self.pdf_buffer = io.BytesIO()
		if pagesize == 'A4':
			self.pagesize = A4
		elif pagesize == 'A5':
			self.pagesize = A5
		self.width = self.pagesize[0]
		self.height = self.pagesize[1]
		self.styles = self.styles()
	
	def styles(self):
		'''Getting and changing styles'''
		styles = getSampleStyleSheet()
		styles.add(ParagraphStyle('h1', parent=styles['Heading1'], fontSize=18, leading=10))
		styles.add(ParagraphStyle('h2', parent=styles['Heading2'], fontSize=12, leading=12))
		styles.add(ParagraphStyle('h2s', parent=styles['Heading2'], fontSize=8, leading=10, textColor='grey'))
		styles.add(ParagraphStyle('h3', parent=styles['Heading3'], fontSize=8, leading=10))
		styles.add(ParagraphStyle('h4', parent=styles['Heading4'], fontSize=10, leading=12))
		styles.add(ParagraphStyle('h6c', parent=styles['Heading6'], alignment=1, fontSize=8, leading=12))
		styles.add(ParagraphStyle('regular', parent=styles['Normal'], fontSize=12, leading=14))
		styles.add(ParagraphStyle('small', parent=styles['Normal'], fontSize=10, leading=12))
		styles.add(ParagraphStyle('body', parent=styles['BodyText'], fontSize=11, leading=12))
		styles.add(ParagraphStyle('right', parent=styles['Normal'], alignment=2))
		styles.add(ParagraphStyle('centered', parent=styles['Normal'], alignment=TA_CENTER))
		styles.add(ParagraphStyle('signature', parent=styles['Normal'], alignment=1, fontSize=10, leading=10, bold=1))
		styles.add(ParagraphStyle('small-centered', parent=styles['Normal'], alignment=1, fontSize=8, leading=8,
		                          textColor='grey'))
		styles.add(
			ParagraphStyle('footer', parent=styles['Heading3'], alignment=2, fontSize=10, leading=8, textColor='grey'))
		styles.add(ParagraphStyle('small-right', parent=styles['Normal'], alignment=2, fontSize=8, leading=8,
		                          textColor='grey'))
		return styles
	
	
	#
	# def build_pdf(self, context={}):
	# 	from InSights.apps.care.models import Prescription, Complaint, Visit
	# 	self.context = context
	# 	doc = SimpleDocTemplate(
	# 		self.pdf_buffer,
	# 		# There are four possible values of alignment, defined as constants in the module reportlab.lib.enums.
	# 		# These are TA_LEFT, TA_CENTER or TA_CENTRE, TA_RIGHT and TA_JUSTIFY, with values of 0, 1, 2 and 4 respectively.
	# 		alignment=4,
	# 		pagesize=self.pagesize,
	# 		width=self.width,
	# 		height=self.height,
	# 		fontName='Helvetica',
	# 		topMargin=self.height * 0.05,
	# 		leftMargin=self.width * 0.05,
	# 		rightMargin=self.width * 0.05,
	# 		bottomMargin=self.height * 0.075,
	# 		spaceAfter=10,
	# 		)
	# 	flowables = []
	# 	if self.context:
	# 		if self.context['plan']:
	# 			plan = self.context['plan']
	# 			patient = plan.relation.patient
	# 			prescriptions = get_list_or_404(Prescription, patient=patient, ongoing=True)
	# 			doctor = plan.relation.professional
	# 			flowables.append(Paragraph(f'{patient}', self.styles['h1T'] ))
	# 			flowables.append(Paragraph(f'Plano Terapêutico com  {doctor} do dia {context["date"]}', self.styles['h2TS']))
	# 			flowables.append(LineFlowable(doc.width))
	#
	# 			if plan.treatment_plan:
	# 				flowables.append(Spacer(0, 15))
	# 				subTitle, listItems = plan.plan_info()
	# 				orientations = []
	# 				for item in listItems:
	# 					orientations.append(ListItem(Paragraph(item, self.styles['regular']), bulletColor='red'))
	# 				flowables.append(Paragraph(subTitle, self.styles['h3T']))
	# 				flowables.append(ListFlowable(orientations, bulletType='bullet', start='square'))
	#
	#
	# 			if prescriptions:
	# 				flowables.append(Spacer(0, 15))
	# 				listItems = []
	# 				flowables.append(Paragraph('''PRESCRIÇÕES:''', self.styles['h3T']))
	# 				for med in prescriptions:
	# 					listItems.append(ListItem(Paragraph(med.__str__(), self.styles['regular']), bulletColor='green'))
	# 				flowables.append(ListFlowable(listItems, bulletType='bullet', start='circle'))
	#
	# 			if plan.next_visit_notes or plan.next_visit_datetime or plan.next_visit_days:
	# 				flowables.append(Spacer(0, 15))
	# 				nextVisitList = plan.next_visit_info()
	# 				listItems = []
	# 				flowables.append(Paragraph('''PARA O PRÓXIMO ENCONTRO:''', self.styles['h3T']))
	# 				for item in nextVisitList:
	# 					listItems.append(ListItem(Paragraph(item, self.styles['regular']), bulletColor='blue'))
	# 				flowables.append(ListFlowable(listItems, bulletType='bullet', start='diamond'))
	# 			spacer = Spacer(0, 35)
	# 			signature = Paragraph(f'{doctor}', self.styles['signature'])
	# 			specialty = Paragraph(f'Psiquiatra Geral e da Infância e Adolescência', self.styles['small-centered'])
	# 			register = Paragraph(f'CRMGO 9553 / CRMDF 12132', self.styles['small-centered'])
	# 			flowables.append(spacer)
	# 			flowables.append(signature)
	# 			flowables.append(specialty)
	# 			flowables.append(register)
	#
	# 		if self.context['followup']:
	# 			visit = self.context['followup']
	# 			visit_date = visit.visit_date.strftime('%d/%m/%Y')
	# 			patient = visit.relation.patient
	# 			flowables.append(Paragraph(f'{patient}', self.styles['h1T']))
	# 			flowables.append(Spacer(0, 15))
	# 			flowables.append(LineFlowable(doc.width))
	# 			flowables.append(Paragraph(f'VISITA MÉDICA {visit_date}', self.styles['h2T']))
	# 			content = visit.visit_text_composition()
	# 			flowables.append(Paragraph(f'{content}', self.styles['body']))
	# 			flowables.append(Spacer(0, 7))
	# 			content = visit.treatment_plan()
	# 			flowables.append(Paragraph(f'{content}', self.styles['body']))
	#
	#
	# 		if self.context['visit']:
	# 			visit = self.context['visit']
	# 			visit_date = visit.visit_date.strftime('%d/%m/%Y')
	# 			patient = visit.relation.patient
	# 			doctor = visit.relation.professional
	# 			flowables.append(Paragraph(f'{patient}', self.styles['h1T']))
	# 			flowables.append(LineFlowable(self.width))
	# 			flowables.append(Paragraph(f'VISITA MÉDICA {visit_date}', self.styles['h2T']))
	#
	# 			if visit.visit_notes:
	# 				notes = f'{visit.visit_notes}'
	# 				flowables.append(Paragraph('''Notas''', self.styles['h3T']))
	# 				flowables.append(Paragraph(notes, self.styles['body']))
	#
	#
	# 			if visit.patient_examination:
	# 				notes = f'{visit.visit_notes}'
	# 				flowables.append(Paragraph('''Exame do Paciente''', self.styles['h3T']))
	# 				flowables.append(Paragraph(notes, self.styles['regular']))
	#
	# 			if Complaint.objects.filter(visit=visit):
	# 				flowables.append(Paragraph('''Queixas''', self.styles['h3T']))
	# 				complaints = []
	# 				for c in Complaint.objects.filter(visit=visit):
	# 					t, d = '', ''
	# 					if c.complaint and c.intensity:
	# 						t = f'{c.complaint} (intensidade: {c.get_intensity_display()})'.capitalize()
	# 					elif c.complaint:
	# 						t = f'{c.complaint}'.capitalize()
	# 					if c.description:
	# 						d = f'{c.description}'
	# 					complaints.append(ListItem(Paragraph(f'{t} -> {d}', self.styles['regular']), bulletColor='yellow'))
	# 				flowables.append(ListFlowable(complaints, bulletType='bullet'))
	#
	# 			spacer = Spacer(0, 35)
	# 			signature = Paragraph(f'{doctor.name}', self.styles['signature'])
	# 			specialty = Paragraph(f'{doctor.specialty}', self.styles['small-centered'])
	# 			register = Paragraph(f'{doctor.professional_register}', self.styles['small-centered'])
	# 			flowables.append(spacer)
	# 			flowables.append(signature)
	# 			flowables.append(specialty)
	# 			flowables.append(register)
	#
	# 	doc.build(
	# 		flowables,
	# 		onFirstPage=self._header_footer,
	# 		onLaterPages=self._header_footer,
	# 		)
	# 	# Get the value of the BytesIO buffer and write it to the response.
	# 	pdf = self.pdf_buffer.getvalue()
	# 	self.pdf_buffer.close()
	# 	return pdf
	
	
	def build_followup(self, context={}):
		self.context = context
		doc = SimpleDocTemplate(
			self.pdf_buffer,
			# There are four possible values of alignment, defined as constants in the module reportlab.lib.enums.
			# These are TA_LEFT, TA_CENTER or TA_CENTRE, TA_RIGHT and TA_JUSTIFY, with values of 0, 1, 2 and 4 respectively.
			alignment=4,
			pagesize=self.pagesize,
			width=self.width,
			height=self.height,
			fontName='Helvetica',
			topMargin=self.height * 0.05,
			leftMargin=self.width * 0.05,
			rightMargin=self.width * 0.05,
			bottomMargin=self.height * 0.075,
			spaceAfter=10,
		)
		flowables = []
		flowables.append(Paragraph(f'{context["patient"]}', self.styles['h1T']))
		flowables.append(Spacer(0, 10))
		flowables.append(LineFlowable(doc.width))
		flowables.append(Paragraph(f'Visita dia {context["date_formated"]}', self.styles['h2T']))
		content = context['visit'].start_of_visit()
		flowables.append(Paragraph(f'{content}', self.styles['body']))
		content = context['visit'].actual_disease()
		flowables.append(Paragraph(f'{content}', self.styles['body']))
		content = context['visit'].end_visit()
		flowables.append(Paragraph(f'{content}', self.styles['body']))
		
		doc.build(
			flowables,
			onFirstPage=self._header_footer,
			onLaterPages=self._header_footer,
		)
		# Get the value of the BytesIO buffer and write it to the response.
		pdf = self.pdf_buffer.getvalue()
		self.pdf_buffer.close()
		return pdf


# ----------------------------------------------------------------------
def create_pdf():
	"""
	Create a pdf
	"""
	story = []
	doc = SimpleDocTemplate("test.pdf", pagesize=letter)
	styles = getSampleStyleSheet()
	spacer = Spacer(0, 0.25 * inch)
	
	text = 'PLANO TERAPÊUTICO'
	ptext = f'<font size="12">{text}</font>'
	story.append(Paragraph(ptext, styles["Normal"]))
	story.append(spacer)
	
	line = LineFlowable(doc.width)
	story.append(line)
	story.append(spacer)
	
	ptext = '<font size="12">%s</font>' % "Section #2"
	story.append(Paragraph(ptext, styles["Normal"]))
	
	doc.build(story)


# ----------------------------------------------------------------------
if __name__ == "__main__":
	create_pdf()
