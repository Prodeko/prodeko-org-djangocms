from django.shortcuts import render_to_response


def handler500(request, template_name="500.html"):
    response = render_to_response("500.html")
    response.status_code = 500
    return response
