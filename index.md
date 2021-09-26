## Global River Runner


[![](https://internetofwater.org/wp-content/uploads/2019/12/iow_logo_horizontal_rgb_TM_header.png)](https://internetofwater.org/)[![](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/USGS_logo_green.svg/320px-USGS_logo_green.svg.png)](https://www.usgs.gov/mission-areas/water-resources)


The [Global River Runner](https://river-runner-global.vercel.app/) is a vizualization simulating the path a raindrop would take, assuming it runs off into a stream and from then on to a terminating location, likely an inland water body or the ocean. The front end visualization was developed by [Sam Learner](https://samlearner.com). 
The [back end](https://merit.internetofwater.app) is developed by [Dave Blodgett](https://www.usgs.gov/staff-profiles/david-l-blodgett?qt-staff_profile_science_products=3#qt-staff_profile_science_products), [Kyle Onda](https://internetofwater.org/about/people/kyle-onda/) and [Ben Webb](https://github.com/webb-ben) as a demonstrator of several key aspects of the [Internet of Water](https://internetofwater.org) project, including leveraging open data, open source software, and open standards to create innovative water information products and applications.

### Open Data

The "rivers run" by the application are available as a database for download [here](https://www.sciencebase.gov/catalog/item/614a8864d34e0df5fb97572d). This database is a simplification of [MERIT-Basins](https://www.reachhydro.org/home/params/merit-basins) optimized for web viewing, and augmented with river names from the [Natural Earth Rivers + lakes centerlines dataset](https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-rivers-lake-centerlines/). MERIT-Basins is a global vector hydrography dataset derived from the [MERIT-Hydro raster data product](http://hydro.iis.u-tokyo.ac.jp/~yamadai/MERIT_Hydro/), which itself is derived from the [MERIT Digital Elevation Model](http://hydro.iis.u-tokyo.ac.jp/~yamadai/MERIT_DEM/index.html). All of these data are published with an open [Creative Commons CC BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/) License, which allows them to be used for free for science as well as for noncommercial creative works such as this one. 


### Open Source Software

The back end API is served by [pygeoapi](https://pygeoapi.io), an open-source python server for publishing geospatial data and web-based geoprocessing jobs. The API interacts with the data in a [PostGIS](https://postgis.net)/[PostgreSQL](https://www.postgresql.org) database. These are all incredibly useful, free and open source technologies for creating spatial data infrastructure that support innovative web applications. 

Our API for tracing downstream river flowpaths is documented in the OpenAPI standard [here](https://merit.internetofwater.app/openapi?f=html#/river-runner/executeRiver-runnerJob). The code underlying the API is available [here](https://github.com/webb-ben/pygeoapi/blob/river-runner/pygeoapi/process/river_runner.py).

The basic use of the API is to provide the latitude and longitude of a start point, and you will be returned a geojson file of line segments representing the flowpath downstream on the start point. The format is as below:

```
https://merit.internetofwater.app/processes/river-runner/execution?lat=<latitude>&lng=<longitude>
```

For example, trace the path from [Humayun's Tomb](https://www.google.com/maps/place/Humayun’s+Tomb/@28.5827539,77.1890893,12.24z/data=!4m13!1m7!3m6!1s0x390cfd5b347eb62d:0x52c2b7494e204dce!2sNew+Delhi,+Delhi,+India!3b1!8m2!3d28.6139391!4d77.2090212!3m4!1s0x390ce31ce8460ba7:0xb9f1ba2d3bdfa80d!8m2!3d28.5932848!4d77.2507492) in New Delhi, India to the mouth of the Ganges:

```
https://merit.internetofwater.app/processes/river-runner/execution?lat=28.5827539&lng=77.1890893
```


The entire API and database stack can be deployed on your own, see the [github repository](https://github.com/ksonda/global-river-runner) for more details. If you have docker and git installed, it's as easy as:

```
git clone https://github.com/ksonda/global-river-runner.git
cd pygeoapi
wget https://prod-is-usgs-sb-prod-publish.s3.amazonaws.com/614a8864d34e0df5fb97572d/merit_plus.sql.gz
docker-compose up -d
```

Wait some time for the database to load, then point your browser to http://localhost:5050 to explore the pygeoapi server.



### Open Standards

The River Runner API is implemented as a combination of two API standards published by the [Open Geospatial Consortium](https://www.ogc.org). 

The River Runner API is compliant with the [OGC-API Processes (OAProc)](https://ogcapi.ogc.org/processes/) standard. Development of this standard is [ongoing](https://github.com/opengeospatial/ogcapi-processes), but it promises to provide a simple, useful framework for URL patterns that allow for the retrieval of metadata describing a given geoprocessing API and executing jobs.

The River Runner API interacts with the underlying database via another API compliant with the [OGC-API Features (OAF)](https://ogcapi.ogc.org/features/) standard. This standard specifies simplie URL patterns to discover metadata about, and retrieve subsets of geospatial vector datasets. It is the successor to the well-known Web Feature Service.



### Prior work

#### U.S. River Runner
This application is a derivative of the original [River Runner](https://river-runner.samlearner.com), which offers the same visualization for the contiguous United States and was also developed by [Sam Learner](https://samlearner.com).

#### Network-Linked Data Index
The original River Runner relies on the U.S. Geological Survey's [Network-Linked Data Index (NLDI)]https://waterdata.usgs.gov/blog/nldi-intro/) API, which allows upstream and downstream traces of the US National Hydrography as represented by [NHDPlus Version 2](https://www.epa.gov/waterdata/nhdplus-national-hydrography-dataset-plus). The NLDI is an open system that allows external datasets (such as water quality monitoring stations) to be indexed to the national hydrography. The NLDI itself is derived from the [Upstream/Downstream discovery tools](https://watersgeo.epa.gov/openapi/waters/#/Discovery) of the U.S. Environmental Protection Agency [WATERS](https://www.epa.gov/waterdata/waters-watershed-assessment-tracking-environmental-results-system) data system, which indexes many EPA data products to NHDPlus Version 2. The NLDI is developed as an [open source project](https://github.com/ACWI-SSWD).

### Future Work
