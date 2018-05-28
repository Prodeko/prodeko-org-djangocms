from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage


def main(request):
    tiedostot = Tiedosto.objects.all()
    return render(request, 'tiedostot.html', {
        'tiedostot': tiedostot,
    })

def download(request, file_name):
    file_object = Tiedosto.objects.get(file_name = 'file_name')
    file_path = file_object.actual_file.path
    
    file_wrapper = FileWrapper(file(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s/' % smart_str(file_name)
    return response
