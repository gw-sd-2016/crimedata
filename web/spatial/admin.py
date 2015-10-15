from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from spatial.models import CrimeType, Incident

# (Very simple) default associations of the models to the builtin Admin Site
# This will allow for basic validation during model design


class IncidentAdminOverride(gis_admin.OSMGeoAdmin):
    default_lon = -77.049619
    default_lat = 38.899141
    readonly_fields = ('lat', 'lon')


admin.site.register(CrimeType)
admin.site.register(Incident, IncidentAdminOverride)
