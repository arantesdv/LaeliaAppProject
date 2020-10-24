from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER



class Styles:
	
	@staticmethod
	def compile():
		styles = getSampleStyleSheet()
		styles.add(ParagraphStyle('h1T', parent=styles['Heading1'], fontSize = 18, leading=10,))
		styles.add(ParagraphStyle('h2T', parent=styles['Heading2'], fontSize = 12, leading=12,))
		styles.add(ParagraphStyle('h2s',parent=styles['Heading2'],fontSize = 8,leading=10,textColor='grey',))
		styles.add(ParagraphStyle('h3T',parent=styles['Heading3'],fontSize=8,leading=10,))
		styles.add(ParagraphStyle('h4T',parent=styles['Heading4'],fontSize=10,leading=12,))
		styles.add(ParagraphStyle('h6T',parent=styles['Heading6'],fontSize=10,leading=12, textColor='red'))
		styles.add(ParagraphStyle('regular',parent=styles['Normal'],fontSize=12,leading=14,))
		styles.add(ParagraphStyle('small',parent=styles['Normal'],fontSize=8,leading=10,))
		styles.add(ParagraphStyle('body',parent=styles['BodyText'],fontSize=10,leading=12,))
		styles.add(ParagraphStyle('right',parent=styles['Normal'],alignment=2))
		styles.add(ParagraphStyle('signature',parent=styles['Normal'],alignment=1, fontSize=10, leading=10, bold=1))
		styles.add(ParagraphStyle('small-centered',parent=styles['Normal'],alignment=1, fontSize=8, leading=8, textColor='grey'))
		styles.add(ParagraphStyle('header',parent=styles['Heading2'],alignment=0, fontSize=12, leading=12, textColor='grey'))
		styles.add(ParagraphStyle('footer',parent=styles['Heading3'],alignment=2, fontSize=10, leading=10, textColor='grey'))
		styles.add(ParagraphStyle('small-right',parent=styles['Normal'],alignment=2, fontSize=8, leading=8, textColor='grey'))
		return styles