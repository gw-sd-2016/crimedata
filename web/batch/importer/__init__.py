import abc
from spatial.models import Incident, CrimeType
from batch.importer.exceptions import InvalidSourceException
from django.contrib.gis.geos import GEOSGeometry

class ImporterBase(object, metaclass=abc.ABCMeta):
    __source_code = ""

    def set_source_code(self, code):
        valid_source_codes = dict(Incident.SOURCE_CHOICES)
        if code not in valid_source_codes:
            raise InvalidSourceException(str(code))

        self.__source_code = code

    @abc.abstractmethod
    def load_data(self):
        return

    # @abc.abstractmethod
    def insert_record(self, type, time, lat, lon, narrative):
        if not isinstance(type, CrimeType):
            type = CrimeType.objects.get(pk=type)

        geos_coord_str = "POINT(%s %s)" % (lon, lat)
        geos_coord = GEOSGeometry(geos_coord_str)

        rec = Incident.objects.create(
            date_time=time,
            incident_type=type,
            point=geos_coord,
            narrative=narrative,
            import_source=self.__source_code
        )

        return rec