# Instructions

## Briefing

Your task is to deploy METAR processing service (a django application exposing REST API) 
on the Kubernetes cluster in the sample GCP project.

METARs are messages reporting the weather situations on the stations (usually airports). 
The full deployment should consist of the following parts:
* database (Postgres),
* RabbitMQ (message broker for celery),
* Python web process (handling HTTP API connections),
* Python asynchronous worker process (celery worker),
* Celery beat process (single!).

Just for your information, the METAR service is connecting to this link every 1 minute:
```https://www.aviationweather.gov/adds/dataserver_current/current/metars.cache.xml```

Reads all METAR messages, which are formatted like this:
```
<METAR>
    <raw_text>KANJ 041755Z AUTO 13013G24KT 10SM FEW070 OVC100 02/M06 A2965 RMK AO2 SLP048 T00221056 10028 21044 58031</raw_text>
    <station_id>KANJ</station_id>
    <observation_time>2021-02-04T00:05:00Z</observation_time>
    <latitude>46.47</latitude>
    <longitude>-84.37</longitude>
    <temp_c>2.2</temp_c>
    <dewpoint_c>-5.6</dewpoint_c>
    <wind_dir_degrees>130</wind_dir_degrees>
    <wind_speed_kt>13</wind_speed_kt>
    <wind_gust_kt>24</wind_gust_kt>
    <visibility_statute_mi>10.0</visibility_statute_mi>
    <altim_in_hg>29.648623</altim_in_hg>
    <sea_level_pressure_mb>1004.8</sea_level_pressure_mb>
    <quality_control_flags>
    <auto>TRUE</auto>
    <auto_station>TRUE</auto_station>
    </quality_control_flags>
    <sky_condition sky_cover="FEW" cloud_base_ft_agl="7000"/>
    <sky_condition sky_cover="OVC" cloud_base_ft_agl="10000"/>
    <flight_category>VFR</flight_category>
    <three_hr_pressure_tendency_mb>-3.1</three_hr_pressure_tendency_mb>
    <maxT_c>2.8</maxT_c>
    <minT_c>-4.4</minT_c>
    <metar_type>METAR</metar_type>
    <elevation_m>220.0</elevation_m>
</METAR>
```
Stores each of those message in django Metar model (DB) together with FK relation of SkyConditions.
Eventually expose an endpoint `GET /metars/{timestamp}/` that returns list of the latest metars 
on each station.

You can also inspect METARs via the django admin (http://localhost:8000/admin/).

For your convenience we added a Makefile that can help you start the service locally
(pre-requirements: gnu make, docker and docker-compose):
 1. `make build` (build docker images)
 1. `make migrate` (perform django migration)
 1. `make superuser` (create user for django admin)
 1. `make web` (run django HTTP server)
 1. `make celery` (run celery asynchronous tasks worker)
 1. Navigate to http://localhost:8000/ (swagger) and/or http://localhost:8000/admin/ (django admin)


You can confirm if application is running correctly by doing the following GET call:
* Calculate latest timestamp (e.g. `1612400000`)
* Call GET http://localhost:8000/metars/1612400000/
* Expect result HTTP 200 response like:
    ```
   [...
        {
          "raw_text": "KANJ 041755Z AUTO 13013G24KT 10SM FEW070 OVC100 02/M06 A2965 RMK AO2 SLP048 T00221056 10028 21044 58031",
          "station_id": "KANJ",
          "observation_time": "2021-02-04T00:05:00Z",
          "latitude": 46.47,
          "longitude": -84.37,
          "temp_c": 2.2,
          "dewpoint_c": -5.6,
          "wind_dir_degrees": 130,
          "wind_speed_kt": 13,
          "sky_conditions": [
            { "sky_cover": "FEW", "cloud_base_ft_agl": "7000" },
            { "sky_cover": "OVC", "cloud_base_ft_agl": "10000" }
          ]
        },
   ...]
   ```

## Assignment Task
Assignment is split into 3 stages with with increasing difficulty. Probably you won't be able to complete all the tasks. Finish as much as you can.


### Stage 1 (basics; extra point on using Terraform)
1. Setup kubernetes cluster on GKE.
1. Release docker image to the GCR registry.
1. Deploy Postgres (Cloud SQL GCP's service/helm chart or yaml).
1. Prepare kubernetes yaml job file with django migration job (migrate target in the makefile).
1. Deploy RabbitMQ as helm chart or yaml (rabbitmq in docker-compose)
1. Prepare kubernetes yaml deployment file with celery worker (celery target in the makefile). 
1. Prepare kubernetes yaml deployment file with web (server target in the makefile). 
1. Create django admin user in the deployed application;

After those steps application is considered as fully deployed.

### Stage 2
1. Add probes for the web server.
2. Setup requests/limits properly.
3. Use wsgi production server instead of Django's development server. Use settings which will give the best perfromance r/s.
4. Prepare/Deploy any metrics monitoring platform (preferably grafana + prometheus or stackdriver metrics).
5. Implement a metric counter for amount of METARs added (number of objects processed) and a metric for the latency of `GET /metars/{timestamp}/` endpoint. Present metrics in a metrics dashboard.

### Stage 3
1. Reduce size of docker images.
1. Find possible database bottleneck in the endpoint  `GET /metars/{timestamp}/` and add database index addressig potential issues.
1. Implement k8s autoscalers for web and celery pods.
1. Prepare CI/CD pipeline which will redeploy application on any change in the code. Recommended tools: github actions, GCP's Cloud Build, travis or CircleCI.

### Stage 4
1. Any improvements which you consider as important.

---
Additional notes:

1. You are free to use other tools than mentioned.
