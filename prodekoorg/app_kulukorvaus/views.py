import json
from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import KulukorvausForm, KulukorvausPerustiedotForm
from .models import Kulukorvaus
from .printing import KulukorvausPDF


def generate_kulukorvaus_pdf(model_perustiedot, models_kulukorvaukset):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="kulukorvaus.pdf"'

    # Buffer to hold the pdf
    buffer = BytesIO()

    # init KulukorvausPDF defined in printing.py
    kulukorvaus = KulukorvausPDF(model_perustiedot, models_kulukorvaukset, buffer)
    # Print out the pdf based on model data
    pdf = kulukorvaus.print_kulukorvaukset()

    # set the 'pdf' attribute of model KulukorvausPerustiedot
    pdf_file = ContentFile(pdf)
    model_perustiedot.pdf.save('kulukorvaus.pdf', pdf_file)

    # Write pdf to response
    response.write(pdf)
    return response


def show_kulukorvaus_pdf(request):
    fs = FileSystemStorage()
    # filename = '{}-{}-{}'.format(today.strftime('%Y-%m-%d'), form.created_by, form.target)
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
            return response
    else:
        return HttpResponseNotFound('Kulukorvaus '.format(request))


def main_form(request):
    KulukorvausFormset = formset_factory(KulukorvausForm)
    if request.method == 'POST':
        form_perustiedot = KulukorvausPerustiedotForm(request.POST)
        formset = KulukorvausFormset(request.POST, request.FILES)

        is_valid_perustiedot = form_perustiedot.is_valid()
        is_valid_formset = formset.is_valid()

        if is_valid_perustiedot and is_valid_formset:
            models_kulukorvaukset = []
            for form in formset:
                model = form.save()
                models_kulukorvaukset.append(model)

            model_perustiedot = form_perustiedot.save()

            return generate_kulukorvaus_pdf(model_perustiedot, models_kulukorvaukset)
        else:
            print("here")
            return render(request, 'kulukorvaus.html', {'form_perustiedot': form_perustiedot,
                                                        'formset_kulu': formset
                                                        })
    elif request.is_ajax():
        pass
    else:
        form_perustiedot = KulukorvausPerustiedotForm()
        formset = KulukorvausFormset()
        return render(request, 'kulukorvaus.html', {'form_perustiedot': form_perustiedot,
                                                    'formset_kulu': formset
                                                    })
