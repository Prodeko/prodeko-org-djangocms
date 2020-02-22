import json
from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.serializers import serialize
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from PIL import Image

from .forms import EhdokasForm, KysymysForm, VastausForm
from .models import Ehdokas, Kysymys, Virka


class EhdokasCreateView(SuccessMessageMixin, CreateView):
    model = Ehdokas
    success_url = reverse_lazy("app_vaalit:vaalit")
    success_message = "Hakemuksesi virkaan on lähetetty."


class EhdokasDeleteView(SuccessMessageMixin, DeleteView):
    """ Handles 'Ehdokas' model application deleting.

    Raises:
        PermissionDenied: Unauthorized user tried to delete an application that
                          they didn't create.
    """

    model = Ehdokas
    success_url = reverse_lazy("app_vaalit:vaalit")
    success_message = "%(name)s poistettu onnistuneesti."

    def get_object(self, *args, **kwargs):
        """Allow updating the object only if request.user created the application."""
        obj = super(EhdokasDeleteView, self).get_object(*args, **kwargs)
        if obj.auth_prodeko_user != self.request.user:
            raise PermissionDenied
        return obj

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(EhdokasDeleteView, self).delete(request, *args, **kwargs)


class EhdokasUpdateView(UpdateView):
    """ Handles 'Ehdokas' model application updates.

    Raises:
        PermissionDenied: Unauthorized user tried to delete an application that
                          they didn't create.
    """

    model = Ehdokas
    form_class = EhdokasForm
    success_url = reverse_lazy("app_vaalit:vaalit")
    template_name = "forms/vaalit_modify_application_form.html"

    def get_object(self, *args, **kwargs):
        """Allows updating the object only if request.user created the application."""
        obj = super(EhdokasUpdateView, self).get_object(*args, **kwargs)
        if obj.auth_prodeko_user != self.request.user:
            raise PermissionDenied
        return obj

    def form_valid(self, form, *args, **kwargs):
        request = self.request
        context = self.get_context_data()
        ehdokas = self.get_object()
        response = handle_modify_ehdokas(request, context=context, ehdokas=ehdokas)
        return HttpResponseRedirect(self.get_success_url())


@login_required
def delete_kysymys_view(request, pk):
    """Handle question deletions."""
    kysymys = get_object_or_404(Kysymys, pk=pk)
    if kysymys.created_by != request.user:
        raise PermissionDenied
    if request.method == "POST" and request.is_ajax():
        id = kysymys.id
        kysymys.delete()
        return JsonResponse({"delete_kysymys_id": id})
    else:
        return JsonResponse({"delete_kysymys_id": 1})


@login_required
def update_kysymys_view(request, pk):
    """Handle question deletions."""
    kysymys = get_object_or_404(Kysymys, pk=pk)
    if kysymys.created_by != request.user:
        raise PermissionDenied
    if request.method == "POST":
        kysymys.delete()
        return redirect("app_vaalit:vaalit")
    else:
        raise Http404


def crop_pic(uploaded_img, x, y, w, h):
    if not uploaded_img:
        img_url = staticfiles_storage.open("images/misc/anonymous_prodeko.jpg")
        x, y, w, h = 0, 0, 150, 150
        img = Image.open(img_url)
    else:
        img = Image.open(uploaded_img.file)
    area = (x, y, x + w, y + h)
    cropped_img = img.crop(area)
    img_io = BytesIO()
    # Have to use because people might upload them anyways...
    # We get an error if format='JPEG' because png's have alpha channel
    cropped_img.save(fp=img_io, format="PNG")
    buff_val = img_io.getvalue()
    contentFile = ContentFile(buff_val)
    # If no image was provided use anonymous_prodeko.jpg
    name = uploaded_img.name if uploaded_img else "anonymous_prodeko.jpg"
    ret = InMemoryUploadedFile(
        contentFile, None, name, "image/png", cropped_img.tell, None
    )
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


def is_duplicate_application(request, hidden_virka):
    # If the user has already applied to this virka
    # don't create a new ehdokas instance and display a warning message
    if Ehdokas.objects.filter(
        virka__name=hidden_virka, auth_prodeko_user=request.user
    ).exists():
        messages.warning(
            request,
            "Et voi hakea samaan virkaan kahta kertaa, muokkaa edellistä hakemustasi.",
        )
        return True
    else:
        return False


def get_ehdokkaat_json(context, ehdokas):
    # Append the new ehdokas to the ehdokas_json list that is processed in javascript
    ehdokas_new_python = serialize(
        "python",
        [ehdokas],
        use_natural_foreign_keys=True,
        fields=("auth_prodeko_user", "virka"),
    )
    ehdokas_new_json = json.dumps([d["fields"] for d in ehdokas_new_python])
    ehdokas_new = json.loads(ehdokas_new_json)
    ehdokkaat_json = json.loads(context["ehdokkaat_json"])
    ehdokkaat_json.extend(ehdokas_new)  # Extend operates in-place and returns none
    return json.dumps(ehdokkaat_json)


@login_required
def handle_submit_ehdokas(request, context):
    form_ehdokas = EhdokasForm(request.POST, request.FILES)
    # Store the form in context in case there were errors
    context["form_ehdokas"] = form_ehdokas

    if form_ehdokas.is_valid():

        # Get hidden input values from POST
        hidden_virka, x, y, w, h = get_hidden_inputs(request.POST)

        # Check for duplicate application to one Virka by the same Ehdokas
        if is_duplicate_application(request, hidden_virka):
            return redirect("app_vaalit:vaalit")

        # Crop the image using the hidden input x, y, w and h coordinates
        cropped_pic = crop_pic(request.FILES.get("pic"), x, y, w, h)

        # Get the ehdokas object without committing changes to the database.
        # We still need to append pic, user object and foreign key virka object to the ehdokas object.
        ehdokas = form_ehdokas.save(commit=False)
        if cropped_pic:
            ehdokas.pic = cropped_pic
        ehdokas.auth_prodeko_user = request.user
        ehdokas.virka = get_object_or_404(Virka, name=hidden_virka)
        ehdokas.save()

        mark_as_unread(ehdokas.virka.pk)

        context["ehdokkaat_json"] = get_ehdokkaat_json(context, ehdokas)
        context["form_ehdokas"] = form_ehdokas
        return render(request, "vaalit.html", context)
    else:
        # If there are errors show the form by setting it's display to 'block'
        context["style_vaaliApplyForm"] = "display: block;"
        # Return the form with error messages and reder vaalit main page
        return render(request, "vaalit.html", context)


def handle_modify_ehdokas(request, context, ehdokas):
    # Get hidden input values from POST
    hidden_virka, x, y, w, h = get_hidden_inputs(request.POST)

    # Crop the image using the hidden input x, y, w and h coordinates
    cropped_pic = crop_pic(request.FILES.get("pic"), x, y, w, h)

    # Get the ehdokas object without committing changes to the database.
    # We still need to append pic, user object and foreign key virka object to the ehdokas object.
    ehdokas.pic = cropped_pic
    ehdokas.introduction = request.POST.get("introduction")
    ehdokas.name = request.POST.get("name")
    ehdokas.virka = get_object_or_404(Virka, name=hidden_virka)
    ehdokas.save()
    render(request, "vaalit.html", context)


@login_required
def handle_submit_kysymys(request, context):
    """Process posted questions.

    Returns:

    """
    form_kysymys = KysymysForm(request.POST)
    hidden_virka = request.POST.get("hidden-input-virka")

    # Form validation
    if form_kysymys.is_valid():
        kysymys = form_kysymys.save(commit=False)
        kysymys.created_by = request.user

        virka = get_object_or_404(Virka, name=hidden_virka)
        kysymys.to_virka = virka
        kysymys.save()

        context["kysymys"] = kysymys
        context["virka"] = virka
        mark_as_unread(virka.pk)
        html = render_to_string("vaalit_question.html", context, request)
        return HttpResponse(html)
    else:
        raise Http404


@login_required
def handle_submit_answer(request, context):
    form_vastaus = VastausForm(request.POST)
    hidden_kysymys_id = request.POST.get("hidden-input-kysymys")

    # Form validation
    if form_vastaus.is_valid():
        vastaus = form_vastaus.save(commit=False)
        vastaus.to_question = get_object_or_404(Kysymys, id=hidden_kysymys_id)
        vastaus.by_ehdokas = get_object_or_404(
            Ehdokas.objects.filter(virka=vastaus.to_question.to_virka),
            auth_prodeko_user=request.user,
        )
        vastaus.save()

        mark_as_unread(vastaus.to_question.to_virka.pk)
        html = render_to_string("vaalit_answer.html", context, request)

        return redirect("app_vaalit:vaalit")
    else:
        # Return form with error and render vaalit main page
        return render(request, "vaalit.html", context)


@login_required
def mark_as_read(request, pk):
    # Remove "NEW" marking of virka for the user
    virka = get_object_or_404(Virka, pk=pk)
    virka.read_by.add(request.user)
    virka.save()
    return JsonResponse({"mark_as_read": pk})


def mark_as_unread(pk):
    # Mark virka as "NEW" for all users
    virka = get_object_or_404(Virka, pk=pk)
    virka.read_by.clear()
    virka.save()
    return JsonResponse({"mark_as_unread": pk})


@login_required
def main_view(request):
    context = {}
    ehdokkaat = Ehdokas.objects.all()
    virat = Virka.objects.all()
    # ehdokkaat_json is parsed to JSON in the template 'vaalit_question_form.html'
    ehdokkaat_python = serialize(
        "python",
        ehdokkaat,
        use_natural_foreign_keys=True,
        fields=("auth_prodeko_user", "virka"),
    )
    virat_description_python = serialize(
        "python", virat, use_natural_foreign_keys=True, fields=("description")
    )
    ehdokkaat_json = json.dumps([d["fields"] for d in ehdokkaat_python])
    virat_description_json = json.dumps([d["fields"] for d in virat_description_python])
    context["virat_description_json"] = virat_description_json
    context["virat"] = virat
    context["ehdokkaat"] = ehdokkaat
    context["ehdokkaat_json"] = ehdokkaat_json
    context["count_ehdokkaat_hallitus"] = Virka.objects.filter(is_hallitus=True).count()
    context["count_ehdokkaat_toimarit"] = Virka.objects.filter(
        is_hallitus=False
    ).count()
    if request.method == "POST":
        if "submitVirka" in request.POST:
            return handle_submit_ehdokas(request, context)
        elif "submitVastaus" in request.POST:
            return handle_submit_answer(request, context)
        elif "submitKysymys" in request.POST and request.is_ajax():
            return handle_submit_kysymys(request, context)
        else:
            raise Http404
    else:
        context["form_ehdokas"] = EhdokasForm(
            initial={"name": request.user.first_name + " " + request.user.last_name}
        )
        return render(request, "vaalit.html", context)
