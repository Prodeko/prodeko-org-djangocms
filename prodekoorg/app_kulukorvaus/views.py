from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Kulukorvaus, KulukorvausForm
from reportlab.pdfgen import canvas


def generate_kulukorvaus(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


def render_kulukorvaus(request):
    if request.method == 'POST':
        form = KulukorvausForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = KulukorvausForm()
    return render(request, 'kulukorvaus_form.html', {'form': form})
