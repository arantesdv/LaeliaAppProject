from django.views.generic import View, RedirectView
from django.shortcuts import HttpResponse, reverse, get_object_or_404
from django.http import FileResponse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from Laelia.apps.care.models import Visit
from Laelia.apps.base.models import Relation
from . engine import PdfBuilder


class PdfView(View):
    type = None
    date = None
    patient = None
    professional = None
    object = None
    page = None
    title = None
    introduction = None
    section_1 = None
    section_2 = None
    section_3 = None
    finalization = None
    relation = None
    
    def get_pdf_context_data(self, **kwargs):
        self.relation = get_object_or_404(Relation, pk=self.kwargs.get('relation_id'))
        self.patient = self.relation.patient
        self.professional = self.relation.professional
        if self.kwargs.get('visit_id'):
            self.object = get_object_or_404(Visit, pk=self.kwargs.get('visit_id'))
            self.type, self.page = _('Visit'), 'A4'
            self.title, self.introduction = f'Visita {self.object.date}', f'{self.object.subjective}'
            self.section_1, self.section_2, self.section_3 = f'{self.object.objective}', f'{self.object.assessment}', ''
            self.finalization = f'{self.object.plan}'
        elif self.kwargs.get('plan_id'):
            self.type, self.page = _('Treatment Plan'), 'A5'
            self.object = get_object_or_404(Visit, pk=self.kwargs.get('plan_id'))
        elif self.kwargs.get('treatment_certificate_id'):
            self.type, self.page = _('Treatment Certificate'), 'A4'
            self.object = get_object_or_404(Visit, pk=self.kwargs.get('treatment_certificate_id'))
        context = {
            'type': self.type,
            'patient': self.patient,
            'professional': self.professional,
            'object': self.object,
            'kwargs': self.kwargs,
            'main_title': {self.title},
            'introduction': self.introduction,
            'section_1': self.section_1,
            'section_2': self.section_2,
            'section_3': self.section_3,
            'finalization': self.finalization,
            'page': self.page,
        }
        return context


    def get(self, request, *args, **kwargs):
        context = self.get_pdf_context_data(**kwargs)
        type = context['type']
        patient = context['patient']
        professional = context['professional']
        pdf = PdfBuilder(pagesize=context['page'], relation=self.relation, context=context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=f"{type} {patient} {professional}.pdf"'
        response.write(pdf)
        return response