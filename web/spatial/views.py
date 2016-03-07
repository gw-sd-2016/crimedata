from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.http import urlencode
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D
from djgeojson.views import GeoJSONLayerView

import datetime
import json
from spatial.models import CrimeType, Subdivision
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
    sset = None
    interval_indivisible = False
    active_subdivisions = None

    if request.POST:
        bound_nw_lat = float(request.POST.get('nw_lat'))
        bound_nw_lng = float(request.POST.get('nw_lng'))
        P_nw = (bound_nw_lng, bound_nw_lat)

        bound_se_lat = float(request.POST.get('se_lat'))
        bound_se_lng = float(request.POST.get('se_lng'))
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

        sset = Subdivision.objects.filter(
            polygon__within=bounding_polygon
        )

        interval = None
        if ctid_select is not None:
            # Process spatial autocorrelation based on supplied arguments
            interval = request.POST.get("interval")
            date_groups = []
            if interval is not None and interval != "":
                '''
                If the user did not supply an interval, this all is skipped and the
                supplied params (start/end, inc. type) are passed directly to
                stl_process (the spatial autocorrelation processor).

                If the user DID supply an interval, that means that we want to split the
                supplied date range by the interval and run the autocorrelation processor
                on each interval. The results from each interval will then be displayed
                sequentially on the map.
                    Example:
                        Start date: 2015-05-19
                        End date: 2015-05-25
                        Interval: 1
                        Crime type ID: 1

                        This input would run the analysis for incidents of CTID=1
                        for each day (interval=1) in the range, and then pass the results
                        for each day into their own layer on the map. The map UI will then
                        loop through each layer showing the change over time.
                '''
                try:
                    interval = int(request.POST.get("interval"))
                except:
                    raise ValueError("Unable to cast interval to int")

                dt_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                dt_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                date_range_delta = (dt_end_date - dt_start_date)      # type: datetime.timedelta
                date_range_length = date_range_delta.days

                if date_range_length % interval != 0:
                    interval_indivisible = True

                active_subdivisions = []
                current_date = dt_start_date
                while True:
                    current_end_date = current_date + datetime.timedelta(days=interval)
                    if current_end_date > dt_end_date:
                        current_end_date = dt_end_date
                        print("CD = %s CED = %s DED = %s" % (current_date, current_end_date, dt_end_date))

                    print("DR => %s - %s" % (current_date, current_end_date))
                    current_autocorr_result = stl_process(sset, current_date, current_end_date, ctid_select)
                    if len(current_autocorr_result) == len(sset):
                        current_autocorr_result = []
                    print("\tSAC res len = %d" % len(current_autocorr_result))
                    print("\tSAC res mem = %s" % current_autocorr_result)

                    active_subdivisions.append(current_autocorr_result)
                    if current_end_date >= dt_end_date:
                        break
                    current_date = current_end_date
            else:
                # An interval was not selected so just run the analysis against the total date range
                active_subdivisions = [stl_process(sset, start_date, end_date, ctid_select)]
        # print(active_subdivisions)
        # print(start_date, end_date, ctid_select)
        # print(request.POST)

    subdivisons = Subdivision.objects.all() #.filter(display_name__icontains="County")
    active_subdivisions = json.dumps(active_subdivisions)

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
        #print(bounding_polygon.wkt)
        #print(polyring.wkt)

        #print((P_nw, P_ne, P_se, P_sw, P_nw))


        Q = self.model.objects.filter(
            polygon__within=bounding_polygon
        )

        return Q
