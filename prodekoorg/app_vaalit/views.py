from django.db.models import Count
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from .models import Virka, Ehdokas, Kysymys
from .forms import PhotoForm, EhdokasForm


def main_view(request):
    context = {}
    context['ehdokkaat'] = Ehdokas.objects.all()
    context['virat'] = Virka.objects.all()
    context['count_ehdokkaat_hallitus'] = Virka.objects.annotate(ehdokas_count=Count('ehdokkaat')).filter(is_hallitus=True).count()
    context['count_ehdokkaat_toimarit'] = Virka.objects.filter(is_hallitus=False).count()
    if request.method == 'POST':
        form_photo = PhotoForm(request.POST, request.FILES)
        form_ehdokas = EhdokasForm(request.POST, request.FILES)
        context['form_photo'] = form_photo
        context['form_ehdokas'] = form_ehdokas
        if form_photo.is_valid():
            form_photo.save()
            return redirect('vaalit')
        else:
            return render(request, 'vaalit.html', {'context': context})
    else:
        context['form_photo'] = PhotoForm()
        context['form_ehdokas'] = EhdokasForm()
    return render(request, 'vaalit.html', {'context': context})


class VirkaListView(ListView):
    model = Virka
    context_object_name = 'virat'
    template_name = 'vaalit.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VirkaListView, self).get_context_data(**kwargs)
        context['count_ehdokkaat_hallitus'] = Virka.objects.annotate(ehdokas_count=Count('ehdokkaat')).filter(is_hallitus=True).count()
        context['count_ehdokkaat_toimarit'] = Virka.objects.filter(is_hallitus=False).count()
        return context


class EhdokasCreateView(CreateView):
    model = Ehdokas
    fields = ['name', 'introduction', ]
    template_name = 'vaalit_modal_form.html'

    def form_valid(self, form):
        print(request)
        user = self.request.user
        form.instance.user = user
        return super(EhdokasCreateView, self).form_valid(form)
