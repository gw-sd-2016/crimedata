from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.http import urlencode
from djgeojson.views import GeoJSONLayerView
from spatial.models import CrimeType, Subdivision
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D

## temp ##
from batch.ops.autocorr import stl_process


def mapview(request):
    return render_to_response("mapview.html", locals(), context_instance=RequestContext(request))


def mapview2(request):
    # Mapping UI main page
    # Pass in a list of crime types to be used in view JS
    layer_groups = {}
    crime_types = CrimeType.objects.all()

    # for crime_type in crime_types:
    #     layer_groups[crime_type.pk] = {
    #         "display_name": crime_type.friendly_name,
    #         "color": "red",
    #         "db_id": str(crime_type.pk),
    #     }

    start_date = request.POST.get("start")
    end_date = request.POST.get("end")
    ctid_select = request.POST.get("ctid")

    if ctid_select is not None:
        active_subdivisions = stl_process(start_date, end_date, ctid_select)
    else:
        active_subdivisions = ()
    # print(active_subdivisions)
    # print(start_date, end_date, ctid_select)
    # print(request.POST)

    subdivisons = Subdivision.objects.all() #.filter(display_name__icontains="County")

    return render_to_response("mapview2.html", locals(), context_instance=RequestContext(request))


def subdivs(request):
    return render_to_response("subdivs.html", locals(), context_instance=RequestContext(request))


class IncidentTypeMapLayer(GeoJSONLayerView):
    # Override queryset generator in GeoJSON CBV to allow filtering on query
    def get_queryset(self):
        crime_type_id = self.request.GET.get('ctid')
        bound_nw_lat = self.request.GET.get('nw_lat')
        bound_nw_lng = self.request.GET.get('nw_lng')
        bound_se_lat = self.request.GET.get('se_lat')
        bound_se_lng = self.request.GET.get('se_lng')
        zoom_level = self.request.GET.get('zoom')

        Q = self.model.objects.filter(
            incident_type__pk=crime_type_id,
            lat__gte=float(bound_se_lat),
            lat__lte=float(bound_nw_lat),
            lon__gte=float(bound_nw_lng),
            lon__lte=float(bound_se_lng),
        )[:1500]  # TODO: fix - Temporarily limit max result to 1500

        return Q


class SubdivisionMapLayer(GeoJSONLayerView):
    # Override queryset generator in GeoJSON CBV to allow filtering on query
    def get_queryset(self):
        crime_type_id = self.request.GET.get('ctid')
        bound_nw_lat = float(self.request.GET.get('nw_lat'))
        bound_nw_lng = float(self.request.GET.get('nw_lng'))
        P_nw = (bound_nw_lng, bound_nw_lat)

        bound_se_lat = float(self.request.GET.get('se_lat'))
        bound_se_lng = float(self.request.GET.get('se_lng'))
        P_se = (bound_se_lng, bound_se_lat)

        bound_ne_lat = bound_nw_lat
        bound_ne_lng = bound_se_lng
        P_ne = (bound_ne_lng, bound_ne_lat)

        bound_sw_lat = bound_se_lat
        bound_sw_lng = bound_nw_lng
        P_sw = (bound_sw_lng, bound_sw_lat)

        polyring = LinearRing(P_nw, P_ne, P_se, P_sw, P_nw)
        bounding_polygon = Polygon(polyring)
        print(bounding_polygon.wkt)
        #print(polyring.wkt)

        #print((P_nw, P_ne, P_se, P_sw, P_nw))


        Q = self.model.objects.filter(
            polygon__within=bounding_polygon
        )

        return Q
