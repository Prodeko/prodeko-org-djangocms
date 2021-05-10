from requests import get

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators import gzip


@gzip.gzip_page
@login_required
def stream(request):
    """Proxies the kiltiskamera stream to logged in Prodeko users.

    Retrieves the kiltiskamera stream using a GET request and
    returns it with a StreamingHttpResponse.

    Args:
        request: HttpRequest object from Django.

    Returns:
        StreamingHttpResponse of the camera stream.

        If the user isn't logged in, they are redirected to the login url.
    """

    try:
        response = StreamingHttpResponse(
            get(settings.KILTISKAMERA_URL, stream=True),
            content_type="multipart/x-mixed-replace; boundary=BoundaryString",
        )
        response["Cache-Control"] = "no-cache"
        response["Cache-Control"] = "private"
        return response
    except Exception as e:
        img = staticfiles_storage.open("images/kiltiskamera/webcam_offline.jpg")
        response = HttpResponse(img, content_type="image/jpeg")
        return response


@login_required
def index(request):
    """Renders the main kiltiskamera template.

    Retrieves a stream using a GET request and returns it with
    a StreamingHttpResponse.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.

        If the user isn't logged in, they are redirected to the login url.
    """
    return render(request, "kiltiskamera.html")
