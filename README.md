# global-river-runner
Let's make a global river runner

# Use

# Deployment
Deployment requires an instance of [pygeoapi](https://pygeoapi.io) and postgres with PostGIS installed. 

The pygeoapi instance must include the [river-runner](https://github.com/webb-ben/pygeoapi/blob/river-runner/pygeoapi/process/river_runner.py) process as well as [several other modifications](https://github.com/geopython/pygeoapi/compare/master...webb-ben:river-runner).

We have prepared docker containers for both the latest and current stable versions of pygeoapi.

A copy of the hydrography database used is documented and available for download [here](https://www.sciencebase.gov/catalog/item/614a8864d34e0df5fb97572d).

## Cloud 
See the deploy/cloud directory for Dockerfiles and pygeoapi configurations necessary to deploy an appropriately configured pygeoapi container to the cloud service of your choice. Note the need to use environmental variables to connect to wherever you have chosen to deploy the database. The pygeoapi river-runner is designed to be a stateless application, so your database must be deployed separately. 

## Local
See the deploy/local directory for a docker-compose and pygeoapi configuration for a pygeoapi and postgis stack.
