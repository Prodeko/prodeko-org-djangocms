from io import BytesIO

from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Count
from django.shortcuts import redirect, render
from PIL import Image

from .forms import EhdokasForm
from .models import Ehdokas, Kysymys, Virka


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


def main_view(request):
    context = {}
    context['ehdokkaat'] = Ehdokas.objects.all()
    context['virat'] = Virka.objects.all()
    context['count_ehdokkaat_hallitus'] = Virka.objects.annotate(
        ehdokas_count=Count('ehdokkaat')).filter(is_hallitus=True).count()
    context['count_ehdokkaat_toimarit'] = Virka.objects.filter(is_hallitus=False).count()
    if request.method == 'POST':
        form_ehdokas = EhdokasForm(request.POST, request.FILES)

        # Get hidden input values from POST
        post = request.POST
        hidden_virka = post.get("hidden-input-virka")
        x = float(post.get("hidden-crop-x"))
        y = float(post.get("hidden-crop-y"))
        w = float(post.get("hidden-crop-w"))
        h = float(post.get("hidden-crop-h"))

        # Store the form in context in case there were errors
        context['form_ehdokas'] = form_ehdokas

        if form_ehdokas.is_valid():
            # The original image that was uploaded, has for example .file and .name attributes
            uploaded_img = request.FILES['pic']
            # Crop the image using the hidden input x, y, w and h coordinates
            cropped_img = crop_uploaded_file(uploaded_img, x, y, w, h)
            ehdokas_cropped_img = InMemoryUploadedFile(cropped_img, None, uploaded_img.name, 'image/png', cropped_img.tell, None)
            # Get the ehdokas object without committing changes to the database.
            # We still need to append pic and foreign virka to the object.
            ehdokas = form_ehdokas.save(commit=False)
            ehdokas.pic = ehdokas_cropped_img
            v1 = Virka.objects.get(name=hidden_virka)
            # Saving here is mandatory to make the .add() method work.
            ehdokas.save()
            ehdokas.virka.add(v1)
            ehdokas.save()

            return redirect('vaalit')
        else:
            # Return form with error messages and reder vaalit main page
            return render(request, 'vaalit.html', {'context': context})
    else:
        context['form_ehdokas'] = EhdokasForm()
    return render(request, 'vaalit.html', {'context': context})
