from rest_framework import serializers
from .models import Metar, SkyCondition


class SkyConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkyCondition
        metar = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
        fields = ["sky_cover", "cloud_base_ft_agl"]


class MetarSerializer(serializers.ModelSerializer):
    sky_conditions = SkyConditionSerializer(many=True, required=False)
    temp_c = serializers.FloatField()
    dewpoint_c = serializers.FloatField()

    class Meta:
        model = Metar

        # Exclude 'wind_gust_kt' field and
        # include embedded 'sky_conditions' list
        fields = [
            "raw_text",
            "station_id",
            "observation_time",
            "latitude",
            "longitude",
            "temp_c",
            "dewpoint_c",
            "wind_speed_kt",
            "wind_dir_degrees",
            "sky_conditions",
        ]

    def create(self, validated_data):
        """
        Allow to create sky_conditions at Metar POST
        by overriding create()
        """
        try:
            sky_conditions_data = validated_data.pop("sky_conditions")
        except KeyError:
            metar = Metar.objects.create(**validated_data)
            return metar

        metar = Metar.objects.create(**validated_data)

        for sky_condition_data in sky_conditions_data:
            SkyCondition.objects.create(metar=metar, **sky_condition_data)

        return metar
