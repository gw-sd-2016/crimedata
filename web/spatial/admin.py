from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from leaflet.admin import LeafletGeoAdmin
from spatial.models import CrimeType, Incident

# (Very simple) default associations of the models to the builtin Admin Site
# This will allow for basic validation during model design


class IncidentAdminOverride(LeafletGeoAdmin):
    readonly_fields = ('lat', 'lon')


class CrimeTypeAdminOverride(admin.ModelAdmin):
    list_display = ('friendly_name', 'severity')
    ordering = ['severity']


admin.site.register(CrimeType, CrimeTypeAdminOverride)
admin.site.register(Incident, IncidentAdminOverride)
