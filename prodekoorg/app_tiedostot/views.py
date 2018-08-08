from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .models import Tiedosto, TiedostoVersio
from wsgiref.util import FileWrapper
import mimetypes
import os
from django.utils.encoding import smart_str


def main(request):
    tiedostot = Tiedosto.objects.all()
    return render(request, 'tiedostot.html', {
        'tiedostot': tiedostot,
    })

def download(request, pk):
    file_object = TiedostoVersio.objects.get(pk = pk)
    file_path = file_object.file.path

    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype)
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename={}'.format(file_object.file.name)
    return response
