from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.http import urlencode
from djgeojson.views import GeoJSONLayerView
from spatial.models import CrimeType
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D


def mapview(request):
    return render_to_response("mapview.html", locals(), context_instance=RequestContext(request))


def mapview2(request):
    # Mapping UI main page
    # Pass in a list of crime types to be used in view JS
    layer_groups = {}
    crime_types = CrimeType.objects.all()

    for crime_type in crime_types:
        layer_groups[crime_type.pk] = {
            "display_name": crime_type.friendly_name,
            "color": "red",
            "db_id": str(crime_type.pk),
        }

    return render_to_response("mapview2.html", locals(), context_instance=RequestContext(request))


class IncidentTypeMapLayer(GeoJSONLayerView):
    # Override queryset generator in GeoJSON CBV to allow filtering on query
    def get_queryset(self):
        crime_type_id = self.request.GET.get('ctid')
        return self.model.objects.filter(incident_type__pk=crime_type_id)