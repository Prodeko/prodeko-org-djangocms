from io import BytesIO
from time import localtime, strftime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .forms import KulukorvausForm, KulukorvausPerustiedotForm
from .models import KulukorvausPerustiedot
from .printing import KulukorvausPDF


@login_required(login_url='/login/')
def download_kulukorvaus_pdf(request, perustiedot_id):
    try:
        model_perustiedot = KulukorvausPerustiedot.objects.get(id=perustiedot_id)
        if not request.user == model_perustiedot.created_by_user:
            raise PermissionDenied
    except KulukorvausPerustiedot.DoesNotExist:
        raise Http404("Reimbursement does not exist")

    # Create the HttpResponse object with the appropriate PDF headers.
    time = strftime("%Y-%m-%d", localtime())
    filename = '{}_kulukorvaus_{}.pdf'.format(time, model_perustiedot.created_by.replace(" ", "_"))
    response = HttpResponse(model_perustiedot.pdf.file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    return response


def add_pdf_to_model(perustiedot_id):
    model_perustiedot = KulukorvausPerustiedot.objects.get(id=perustiedot_id)
    models_kulukorvaukset = model_perustiedot.kulukorvaus_set.all()

    # Buffer to hold the pdf
    buffer = BytesIO()

    # init class KulukorvausPDF defined in printing.py
    kulukorvaus = KulukorvausPDF(model_perustiedot, models_kulukorvaukset, buffer)
    # Print out the pdf based on model data
    pdf = kulukorvaus.print_kulukorvaukset()

    # set the 'pdf' attribute of model KulukorvausPerustiedot
    pdf_file = ContentFile(pdf)
    model_perustiedot.pdf.save('kulukorvaus.pdf', pdf_file)


@login_required(login_url='/login/')
def main_form(request):
    KulukorvausFormset = formset_factory(KulukorvausForm)
    if request.method == 'POST' and request.is_ajax():

        form_perustiedot = KulukorvausPerustiedotForm(request.POST)
        formset = KulukorvausFormset(request.POST, request.FILES)

        is_valid_perustiedot = form_perustiedot.is_valid()
        is_valid_formset = formset.is_valid()

        if is_valid_perustiedot and is_valid_formset:
            model_perustiedot = form_perustiedot.save(commit=False)
            model_perustiedot.created_by_user = request.user
            model_perustiedot.save()

            for form in formset:
                model = form.save(commit=False)
                model.info = model_perustiedot
                model.save()

            add_pdf_to_model(model_perustiedot.id)

            # Successfull form submission - render page displaying
            # info and pdf download link
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
