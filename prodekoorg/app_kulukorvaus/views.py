from io import BytesIO
from time import localtime, strftime

from django.core.files.base import ContentFile
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render

from .forms import KulukorvausForm, KulukorvausPerustiedotForm
from .models import KulukorvausPerustiedot
from .printing import KulukorvausPDF


def download_kulukorvaus_pdf(request, perustiedot_id):
    # TODO access control

    model_perustiedot = KulukorvausPerustiedot.objects.get(id=1)
    models_kulukorvaukset = model_perustiedot.kulukorvaus_set.all()

    # Create the HttpResponse object with the appropriate PDF headers.
    time = strftime("%Y-%m-%d", localtime())
    filename = '{}_kulukorvaus_{}.pdf'.format(time, model_perustiedot.created_by.replace(" ", "_"))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

    # Buffer to hold the pdf
    buffer = BytesIO()

    print(models_kulukorvaukset)
    # init KulukorvausPDF defined in printing.py
    kulukorvaus = KulukorvausPDF(model_perustiedot, models_kulukorvaukset, buffer)
    # Print out the pdf based on model data
    pdf = kulukorvaus.print_kulukorvaukset()

    # set the 'pdf' attribute of model KulukorvausPerustiedot
    pdf_file = ContentFile(pdf)
    model_perustiedot.pdf.save('kulukorvaus.pdf', pdf_file)

    # Write pdf to response
    response.write(pdf)
    #return render(request, 'kulukorvaus.html', {'done': True})
    return response


def main_form(request):
    KulukorvausFormset = formset_factory(KulukorvausForm)
    if request.method == 'POST' and request.is_ajax():

        form_perustiedot = KulukorvausPerustiedotForm(request.POST)
        formset = KulukorvausFormset(request.POST, request.FILES)

        is_valid_perustiedot = form_perustiedot.is_valid()
        is_valid_formset = formset.is_valid()

        if is_valid_perustiedot and is_valid_formset:
            models_kulukorvaukset = []
            model_perustiedot = form_perustiedot.save()

            for form in formset:
                model = form.save(commit=False)
                model.info = model_perustiedot
                model.save()
                models_kulukorvaukset.append(model)

            return render(request, 'kulukorvaus.html', {'done': True,
                                                        'perustiedot_id': model_perustiedot.id
                                                        })
        else:
            
            return render(request, 'kulukorvaus_forms.html', {'form_perustiedot': form_perustiedot,
                                                              'formset_kulu': formset
                                                              }, status=599)
    else:
        form_perustiedot = KulukorvausPerustiedotForm()
        formset = KulukorvausFormset()
        return render(request, 'kulukorvaus.html', {'form_perustiedot': form_perustiedot,
                                                    'formset_kulu': formset
                                                    })
