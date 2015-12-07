from django.db import models
from django.contrib.gis.db import models as gis_models


class CrimeType(models.Model):
    friendly_name = models.CharField(null=False, blank=False, max_length=240)
    severity = models.IntegerField(default=5, null=False, blank=False)

    def __str__(self):
        return self.friendly_name


class Incident(gis_models.Model):
    SOURCE_CHOICES = (
        ("ADM", "Admin UI"),
        ("ARM", "GWPD ARMS"),
        ("CHI", "Chicago OpenData"),
        ("ZZZ", "Other"),
    )

    incident_type = gis_models.ForeignKey(CrimeType, null=True, on_delete=gis_models.SET_NULL)
    date_time = gis_models.DateTimeField(null=False, blank=False)
    point = gis_models.PointField()
    lat = gis_models.DecimalField(max_digits=10, decimal_places=6)
    lon = gis_models.DecimalField(max_digits=10, decimal_places=6)
    narrative = gis_models.CharField(null=True, blank=True, max_length=1024)
    import_source = models.CharField(max_length=3, choices=SOURCE_CHOICES, default="ADM")

    def save(self, *args, **kwargs):
        self.lat = self.point.y
        self.lon = self.point.x

        super(Incident, self).save(*args, **kwargs)

    def __str__(self):
        if self.narrative is None or self.narrative.strip() == "":
            return "%s @ %s" % (self.incident_type, self.date_time)
        else:
            return "%s - %s" % (self.incident_type, self.narrative)

    @property
    def marker_title(self):
        return self.__str__()


class Subdivision(gis_models.Model):
    polygon = gis_models.PolygonField()
    display_name = gis_models.CharField(max_length=255)
    objects = gis_models.GeoManager()
    src_file_index = gis_models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "Subdivision: %s" % self.display_name