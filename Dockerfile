ARG IMAGE=python:3.7.2

FROM ${IMAGE} as build
ENV PYTHONUNBUFFERED 1
RUN apt-get -y update && apt-get install -y binutils libproj-dev gdal-bin libspatialindex-dev && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip --no-cache install cython==0.28.5 --prefix /python-packages --no-warn-script-location
ENV PYTHONPATH $PYTHONPATH:/python-packages/lib/python3.7/site-packages
ADD requirements.txt .
RUN pip --no-cache install -r requirements.txt --prefix /python-packages --no-warn-script-location

########## PRODUCTION STAGE ##########
FROM ${IMAGE}-slim
ENV PYTHONUNBUFFERED 1
ENV PROJECT_DIR /uni-assignment-metars
EXPOSE 8000
CMD ["./start-django.sh"]
WORKDIR $PROJECT_DIR
RUN mkdir static

RUN apt-get -y update && apt-get install --no-install-recommends -y libproj12 libspatialindex-c4v5 libgdal20 && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY --from=build /python-packages /usr/local

ADD . $PROJECT_DIR

ARG COMMIT_REF
ARG BUILD_DATE

ENV APP_COMMIT_REF=${COMMIT_REF} \
    APP_BUILD_DATE=${BUILD_DATE}
