import pytz
from datetime import datetime
from rest_framework import viewsets
from rest_framework import filters
from .models import Metar
from .serializers import MetarSerializer


class MetarViewSet(viewsets.ModelViewSet):
    serializer_class = MetarSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["station_id"]

    def get_queryset(self):
        """
        Should only return Metars with 'observation_time'
        older than a timestamp passed in the url
        """
        try:
            timestamp = self.kwargs["timestamp"]
            utc_dt = datetime.utcfromtimestamp(timestamp)
        except OverflowError:
            return Metar.objects.none()

        aware_utc_dt = utc_dt.replace(tzinfo=pytz.utc)

        return (
            Metar.objects.filter(observation_time__lt=aware_utc_dt)
            .order_by("station_id", "-observation_time")
            .distinct("station_id")
        )
