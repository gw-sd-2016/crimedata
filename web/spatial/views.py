from django.shortcuts import render_to_response

# Create your views here.
from django.template import RequestContext


def mapview(request):
    return render_to_response("mapview.html", locals(), context_instance=RequestContext(request))


def mapview2(request):
    return render_to_response("mapview2.html", locals(), context_instance=RequestContext(request))
