from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from leaflet.admin import LeafletGeoAdmin
from spatial.models import CrimeType, Incident, Subdivision, LocationAlias, LocationAliasSecondaryName

# (Very simple) default associations of the models to the builtin Admin Site
# This will allow for basic validation during model design


class IncidentAdminOverride(LeafletGeoAdmin):
    readonly_fields = ('lat', 'lon')

class SubdivisionAdminOverride(LeafletGeoAdmin):
    pass

class CrimeTypeAdminOverride(admin.ModelAdmin):
    list_display = ('friendly_name', 'severity')
    ordering = ['severity']

class LocationAliasSecondaryNameInline(admin.TabularInline):
    model = LocationAliasSecondaryName

class LocationAliasOverride(admin.ModelAdmin):
    inlines = [
        LocationAliasSecondaryNameInline,
    ]
    ordering = ('primary_display_name',)

admin.site.register(CrimeType, CrimeTypeAdminOverride)
admin.site.register(Incident, IncidentAdminOverride)
admin.site.register(Subdivision, SubdivisionAdminOverride)
admin.site.register(LocationAlias, LocationAliasOverride)