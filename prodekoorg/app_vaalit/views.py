from io import BytesIO

from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.templatetags.static import static
from PIL import Image

from .forms import EhdokasForm, KysymysForm, VastausForm
from .models import Ehdokas, Kysymys, Vastaus, Virka


def crop_uploaded_file(uploaded_img, x, y, w, h):
    img = Image.open(uploaded_img.file)
    area = (x, y, x + w, y + h)
    cropped_img = img.crop(area)
    img_io = BytesIO()
    # Have to use because people might upload them anyways...
    # We get an error if forma='JPEG' because png's have alpha channel
    cropped_img.save(fp=img_io, format='PNG')
    buff_val = img_io.getvalue()
    return ContentFile(buff_val)


def handle_submit_virka(request, context):
    form_ehdokas = EhdokasForm(request.POST, request.FILES)

    # Store the form in context in case there were errors
    context['form_ehdokas'] = form_ehdokas

    if form_ehdokas.is_valid():
        # Get hidden input values from POST
        post = request.POST
        hidden_virka = post.get("hidden-input-virka")
        x = float(post.get("hidden-crop-x"))
        y = float(post.get("hidden-crop-y"))
        w = float(post.get("hidden-crop-w"))
        h = float(post.get("hidden-crop-h"))

        # The original image that was uploaded, has for example .file and .name attributes
        uploaded_img = request.FILES.get('pic', )
        # Crop the image using the hidden input x, y, w and h coordinates
        cropped_img = crop_uploaded_file(uploaded_img, x, y, w, h)
        ehdokas_cropped_img = InMemoryUploadedFile(
            cropped_img, None, uploaded_img.name, 'image/png', cropped_img.tell, None)
        # Get the ehdokas object without committing changes to the database.
        # We still need to append pic and foreign key virka to the object.
        ehdokas = form_ehdokas.save(commit=False)
        ehdokas.pic = ehdokas_cropped_img
        v1 = Virka.objects.get(name=hidden_virka)
        # Saving here is mandatory to make the .add() method work.
        ehdokas.save()
        ehdokas.virka.add(v1)
        ehdokas.save()

        # Redirects to this (main_view) view
        return redirect('/vaalit')
    else:
        context['style_vaaliWrapperApplyForm'] = 'display: block;'
        # Return form with error messages and reder vaalit main page
        return render(request, 'vaalit.html', {'context': context})


def handle_submit_kysymys(request, context):
    form_kysymys = KysymysForm(request.POST)
    context['form_kysymys'] = form_kysymys
    hidden_virka = request.POST.get("hidden-input-virka")
    if form_kysymys.is_valid():

        kysymys = form_kysymys.save(commit=False)

        v1 = Virka.objects.get(name=hidden_virka)
        # Saving here is mandatory to make the .add() method work.
        kysymys.to_virka = v1
        kysymys.save()

        return redirect('/vaalit')
    else:
        # Return form with error and render vaalit main page
        return render(request, 'vaalit.html', {'context': context})


def handle_submit_answer(request, context):
    form_vastaus = AnswerForm(request.POST)
    context['form_vastaus'] = form_vastaus
    if form_vastaus.is_valid():
        vastaus = form_vastaus.save()
        return redirect('/vaalit')
    else:
        # Return form with error and render vaalit main page
        return render(request, 'vaalit.html', {'context': context})


def main_view(request):
    context = {}
    context['ehdokkaat'] = Ehdokas.objects.all()
    context['virat'] = Virka.objects.all()
    context['count_ehdokkaat_hallitus'] = Virka.objects.annotate(
        ehdokas_count=Count('ehdokkaat')).filter(is_hallitus=True).count()
    context['count_ehdokkaat_toimarit'] = Virka.objects.filter(is_hallitus=False).count()
    if request.method == 'POST':
        if 'submitKysymys' in request.POST:
            handle_submit_kysymys(request, context)
        elif 'submitVirka' in request.POST:
            handle_submit_virka(request, context)
        elif 'submitVastaus' in request.POST:
            handle_submit_answer(request, context)
    else:
        context['form_ehdokas'] = EhdokasForm()
    return render(request, 'vaalit.html', {'context': context})
