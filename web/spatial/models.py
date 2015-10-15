from django.db import models
from django.contrib.gis.db import models as gis_models

# Create your models here.
class CrimeType(models.Model):
    friendly_name = models.CharField(null=False, blank=False, max_length=240)
    severity = models.IntegerField(default=5, null=False, blank=False)


class Incident(gis_models.Model):
    incident_type = gis_models.ForeignKey(CrimeType, null=True, on_delete=gis_models.SET_NULL)
    date_time = gis_models.DateTimeField(null=False, blank=False)
    point = gis_models.PointField()
    lat = gis_models.DecimalField(max_digits=10, decimal_places=6)
    lon = gis_models.DecimalField(max_digits=10, decimal_places=6)