FROM geopython/pygeoapi:latest

#Add data directory
RUN mkdir /data

#last updated 2021-09-08 00:07:36 UTC-5 
ADD https://www.hydroshare.org/resource/4a22e88e689949afa1cf71ae009eaf1b/data/contents/merit_plus_simplify.gpkg /data/

#add requirements and mods
COPY ./pygeoapi.config.yml /pygeoapi/local.config.yml
COPY ./schemas.opengis.net /opt/schemas.opengis.net
COPY ./pygeoapi-skin-dashboard /skin-dashboard
