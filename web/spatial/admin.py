from django.contrib import admin
from spatial.models import CrimeType, Incident

# Register your models here.
admin.site.register(CrimeType)
admin.site.register(Incident)