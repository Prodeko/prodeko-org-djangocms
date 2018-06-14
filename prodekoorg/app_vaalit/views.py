import json
import os
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.serializers import serialize
from django.http import (Http404, HttpResponse, HttpResponseForbidden,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from PIL import Image

from .forms import EhdokasForm, KysymysForm, VastausForm
from .models import Ehdokas, Kysymys, Vastaus, Virka


class EhdokasDeleteView(SuccessMessageMixin, DeleteView):
    model = Ehdokas
    success_url = reverse_lazy('app_vaalit:vaalit')
    success_message = "Ehdokas %(name)s poistettu onnistuneesti."

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(EhdokasDeleteView, self).delete(request, *args, **kwargs)


class EhdokasUpdateView(UpdateView):
    model = Ehdokas
    form_class = EhdokasForm
    success_url = reverse_lazy('app_vaalit:vaalit')
    template_name = 'vaalit_modify_application.html'

    def form_valid(self, form, *args, **kwargs):
        request = self.request
        context = self.get_context_data()
        ehdokas = self.get_object()
        response = handle_modify_ehdokas(request, context=context, ehdokas=ehdokas)
        return HttpResponseRedirect(self.get_success_url())


def delete_kysymys_view(request, id):
    kysymys = get_object_or_404(Kysymys, id=id)
    if request.method == 'POST':
        kysymys.delete()
        return redirect('/vaalit')
    else:
        raise Http404


def crop_pic(uploaded_img, x, y, w, h):
    if not uploaded_img:
        img_url_prt = static('images/misc/anonymous_prodeko.jpg')
        img_url_full = settings.BASE_DIR + '/prodekoorg' + img_url_prt
        img = Image.open(img_url_full)
    else:
        img = Image.open(uploaded_img.file)
    area = (x, y, x + w, y + h)
    cropped_img = img.crop(area)
    img_io = BytesIO()
    # Have to use because people might upload them anyways...
    # We get an error if forma='JPEG' because png's have alpha channel
    cropped_img.save(fp=img_io, format='PNG')
    buff_val = img_io.getvalue()
    contentFile = ContentFile(buff_val)
    name = uploaded_img.name if uploaded_img else 'anonymous_prodeko.jpg'
    ret = InMemoryUploadedFile(contentFile, None, name,
                               'image/png', cropped_img.tell, None)
    img.close()
    img_io.close()
    return ret


def get_hidden_inputs(post):
    hidden_virka = post.get("hidden-input-virka")
    x = float(post.get("hidden-crop-x"))
    y = float(post.get("hidden-crop-y"))
    w = float(post.get("hidden-crop-w"))
    h = float(post.get("hidden-crop-h"))
    return hidden_virka, x, y, w, h


def is_duplicate_application(user, hidden_virka):
    # If the user has already applied to this virka
    # don't create a new ehdokas instance and display a warning message
    if Ehdokas.objects.filter(virka__name=hidden_virka, auth_prodeko_user=user).exists():
        messages.warning(request, 'Et voi hakea samaan virkaan kahta kertaa, muokkaa edellistä hakemustasi.')
        return True
    else:
        return False


def get_ehdokkaat_json(context, ehdokas):
    # Append the new ehdokas to the ehdokas_json list that is processed in javascript
    ehdokas_new_python = serialize('python', [ehdokas], use_natural_foreign_keys=True,
                                   fields=('auth_prodeko_user', 'virka'))
    ehdokas_new_json = json.dumps([d['fields'] for d in ehdokas_new_python])
    ehdokas_new = json.loads(ehdokas_new_json)
    ehdokkaat_json = json.loads(context['ehdokkaat_json'])
    ehdokkaat_json.extend(ehdokas_new)  # Extend operates in-place and returns none
    return json.dumps(ehdokkaat_json)


def handle_submit_ehdokas(request, context):
    form_ehdokas = EhdokasForm(request.POST, request.FILES)

    # Store the form in context in case there were errors
    context['form_ehdokas'] = form_ehdokas
    if form_ehdokas.is_valid():

        # Get hidden input values from POST
        hidden_virka, x, y, w, h = get_hidden_inputs(request.POST)

        # Check for duplicate application to one Virka by the same Ehdokas
        if is_duplicate_application(request.user, hidden_virka):
            return

        # Crop the image using the hidden input x, y, w and h coordinates
        cropped_pic = crop_pic(request.FILES.get('pic', ), x, y, w, h)

        # Get the ehdokas object without committing changes to the database.
        # We still need to append pic, user object and foreign key virka object to the ehdokas object.
        ehdokas = form_ehdokas.save(commit=False)
        ehdokas.pic = cropped_pic
        ehdokas.auth_prodeko_user = request.user
        ehdokas.virka = get_object_or_404(Virka, name=hidden_virka)
        ehdokas.save()

        context['ehdokkaat_json'] = get_ehdokkaat_json(context, ehdokas)
        context['form_ehdokas'] = form_ehdokas

        render(request, 'vaalit.html', {'context': context})
    else:
        # If there are errors show the form by setting it's display to 'block'
        context['style_vaaliWrapperApplyForm'] = 'display: block;'
        # Return the form with error messages and reder vaalit main page
        return render(request, 'vaalit.html', {'context': context})


def handle_modify_ehdokas(request, context, ehdokas):
    # Get hidden input values from POST
    hidden_virka, x, y, w, h = get_hidden_inputs(request.POST)

    # Crop the image using the hidden input x, y, w and h coordinates
    cropped_pic = crop_pic(request.FILES.get('pic', ), x, y, w, h)

    # Get the ehdokas object without committing changes to the database.
    # We still need to append pic, user object and foreign key virka object to the ehdokas object.
    # TODO handle name once auth_prodeko is ready
    ehdokas.pic = cropped_pic
    ehdokas.auth_prodeko_user = request.user
    ehdokas.virka = get_object_or_404(Virka, name=hidden_virka)
    ehdokas.save()

    render(request, 'vaalit.html', {'context': context})

def handle_submit_kysymys(request, context):
    form_kysymys = KysymysForm(request.POST)
    context['form_kysymys'] = form_kysymys
    context['form_ehdokas'] = EhdokasForm()
    hidden_virka = request.POST.get("hidden-input-virka")
    if form_kysymys.is_valid():

        kysymys = form_kysymys.save(commit=False)
        kysymys.created_by = request.user
        kysymys.to_virka = get_object_or_404(Virka, name=hidden_virka)
        kysymys.save()

        return redirect('/vaalit')
    else:
        # Return form with error and render vaalit main page
        return render(request, 'vaalit.html', {'context': context})


def handle_submit_answer(request, context):
    form_vastaus = VastausForm(request.POST)
    context['form_vastaus'] = form_vastaus
    context['form_ehdokas'] = EhdokasForm()
    hidden_kysymys_id = request.POST.get("hidden-input-kysymys")
    if form_vastaus.is_valid():
        vastaus = form_vastaus.save(commit=False)

        vastaus.by_ehdokas = get_object_or_404(Ehdokas, auth_prodeko_user=request.user)
        vastaus.to_question = get_object_or_404(Kysymys, id=hidden_kysymys_id)
        vastaus.save()

        return redirect('/vaalit')
    else:
        # Return form with error and render vaalit main page
        return render(request, 'vaalit.html', {'context': context})


def main_view(request):
    context = {}
    ehdokkaat = Ehdokas.objects.all()
    # ehdokkaat_json is parsed to JSON in the template 'vaalit_question_form.html'
    ehdokkaat_python = serialize('python', ehdokkaat, use_natural_foreign_keys=True,
                                 fields=('auth_prodeko_user', 'virka'))
    ehdokkaat_json = json.dumps([d['fields'] for d in ehdokkaat_python])
    context['virat'] = Virka.objects.all()
    context['ehdokkaat'] = ehdokkaat
    context['ehdokkaat_json'] = ehdokkaat_json
    context['count_ehdokkaat_hallitus'] = Virka.objects.filter(is_hallitus=True).count()
    context['count_ehdokkaat_toimarit'] = Virka.objects.filter(is_hallitus=False).count()
    if request.method == 'POST':
        if 'submitKysymys' in request.POST:
            handle_submit_kysymys(request, context)
        elif 'submitVirka' in request.POST:
            handle_submit_ehdokas(request, context)
        elif 'submitVastaus' in request.POST:
            handle_submit_answer(request, context)
    else:
        context['form_ehdokas'] = EhdokasForm()
    return render(request, 'vaalit.html', {'context': context})
