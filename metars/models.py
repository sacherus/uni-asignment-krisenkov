from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
)


class Metar(models.Model):
    """
    METAR report model
    """

    raw_text = models.TextField()

    station_id = models.CharField(max_length=4, validators=[MinLengthValidator(4)])

    observation_time = models.DateTimeField()
    location = models.PointField(geography=True, default=Point(0.0, 0.0))

    temp_c = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(-100.00), MaxValueValidator(70.00)],
    )

    dewpoint_c = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(-100.00), MaxValueValidator(70.00)],
    )

    wind_speed_kt = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(200)]
    )

    wind_dir_degrees = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(360)]
    )

    wind_gust_kt = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(200)]
    )

    @property
    def longitude(self):
        return self.location.x

    @property
    def latitude(self):
        return self.location.y

    def __str__(self):
        return f"{self.station_id}@{self.observation_time}"

    class Meta:
        unique_together = (("observation_time", "station_id"),)


class SkyCondition(models.Model):
    metar = models.ForeignKey(
        Metar, related_name="sky_conditions", on_delete=models.CASCADE
    )
    sky_cover = models.CharField(max_length=50, blank=True, null=True)

    cloud_base_ft_agl = models.IntegerField(
        default=0,
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(330000)],
    )
