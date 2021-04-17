import requests
from xml.etree import ElementTree
from metars.models import Metar, SkyCondition
from django.db.utils import IntegrityError


def process_data(url: str) -> []:
    """
    Download and validate METARS data
    Return list of kwargs to create METAR objects
    """
    response = requests.get(url)
    root = ElementTree.fromstring(response.text)

    # This is a list of tuples with args
    # Looks like this: ({}, [])
    kwargs_list = []

    for metar in root.find("data"):
        """
        If some value is missing, ignore whole METAR
        """
        try:
            raw_text = metar.find("raw_text").text
            station_id = metar.find("station_id").text
            observation_time = metar.find("observation_time").text
            temp_c = metar.find("temp_c").text
            dewpoint_c = metar.find("dewpoint_c").text
            wind_dir_degrees = metar.find("wind_dir_degrees").text
            wind_gust_kt = metar.find("wind_dir_degrees").text
            wind_speed_kt = metar.find("wind_speed_kt").text
            latitude = metar.find("latitude").text
            longitude = metar.find("longitude").text

            sky_conditions = []

            if metar.iter("sky_condition") is not None:
                for sky_condition in metar.iter("sky_condition"):
                    if sky_condition.attrib is not None:
                        sky_conditions.append(sky_condition.attrib)

            kwargs = {
                "raw_text": raw_text,
                "station_id": station_id,
                "observation_time": observation_time,
                "location": f"POINT( {longitude} {latitude})",
                "temp_c": temp_c,
                "dewpoint_c": dewpoint_c,
                "wind_speed_kt": wind_speed_kt,
                "wind_dir_degrees": wind_dir_degrees,
                "wind_gust_kt": wind_gust_kt,
            }

            kwargs_list.append((kwargs, sky_conditions))

        except AttributeError:
            """
            Ignore corrupted data
            """
            pass

    return kwargs_list


def create_METAR_objects(kwargs_list: []) -> None:
    """
    Create non-existing METAR objects
    """
    for kwargs in kwargs_list:
        try:
            metar = Metar.objects.create(**kwargs[0])
            print(f"Storing METAR {metar}")
            for sky_condition_data in kwargs[1]:
                SkyCondition.objects.create(metar=metar, **sky_condition_data)

        except IntegrityError:
            # This mean METAR with given timestamp already exists
            pass
