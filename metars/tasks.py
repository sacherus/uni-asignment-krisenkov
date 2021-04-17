from datetime import timedelta

from celery.task import periodic_task

from .utils import process_data, create_METAR_objects

METARS_URL = (
    "https://www.aviationweather.gov/adds/dataserver_current/current/metars.cache.xml"
)


@periodic_task(run_every=timedelta(minutes=1), ignore_result=True)
def task_process_metars():
    """
    Call process_data to parse XML blob
    Then create METAR objects with given data
    """
    data = process_data(METARS_URL)
    print(f"Checking {len(data)} METARs.")
    create_METAR_objects(data)
