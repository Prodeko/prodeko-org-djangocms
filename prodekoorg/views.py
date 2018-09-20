
from django.core.urlresolvers import reverse
from django.http import (HttpResponseForbidden, HttpResponseNotFound,
                         JsonResponse, StreamingHttpResponse)
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render,
                              render_to_response)
from django.template import RequestContext


def profile(request):
    return render()
