from django.shortcuts import render
from sentry_sdk import capture_message


def handler404(request, exception=None, template_name="404.html"):
    capture_message("Page not found!", level="error")
    response = render(request, "404.html")
    response.status_code = 404
    return response

def handler500(request, template_name="500.html"):
    response = render(request, "500.html")
    response.status_code = 500
    return response
