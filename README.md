# PYRAMID Prepare Data

## About
Reads data from the "read-external" model step and prepares this for feeding into SHETRAN.

Prepares data to go into SHETRAN and HIPIMS
Notes
This code relies on the following code
read_met - reads in 5-minute gridded (composite and processed C-band weather radar from the Met Office ftp server.
read_ea - reads in 15-minute rain gauge data from the EA website API.
read_cs - reads in varying resolution rain gauge data from NGIF and UO APIand accumulates up to 15-minute resolution data.
read_cs_radar - reads in Urban Observatory X-band radar code, processes it and accumulates it up to 15 minutes.
intense_qc - quality controls all gauge data using intense-qc code (Note: this is designed for hourly rain gauge data).
It also requires the bounding box shapefile for HIPIMS and the Tyne mask file for SHETRAN (these are in the static.zip sent on teams).
What does this code do?
Reads in data
Read in radar data (if exists)
Met Office radar data
Urban Observatory radar data
Read in quality controlled rain gauge data (if exists)
Environment Agency rain gauges
Urban Observatory rain gauges
Citizen Science rain gauges
National Green Infrastructure Facility rain gauges
Identifies best data to use
Uses data priority for HIPIMS
Uses data priority for SHETRAN
Grids/merges data
Combines different data types to provide gridded 15-minute rainfall estimates (1km resolution)
Saves data in correct format for models
Clips and saves data in correct format for HIPIMS
Clips and saves data in correct format for SHETRAN
Prioritises data for input into HIPIMS model
High resolution (250m) X-band radar data, merged with rain gauges, which is conditional on Met Office C-band radar data.
High resolution (250m) X-band radar data, conditional on Met Office C-band radar data.
High resolution (250m) X-band radar data, merged with rain gauges.
Merged Met Office radar data and quality controlled rain gauge data.
Met Office radar data.
Gridded quality controlled rain gauge data (IF Environment Agency rain gauge data exists).
NOTE: 1. and 2. are missing as cannot test this whilst the Urban Observatory radar is down for maintenence and API is not working.

Prioritises data for input into SHETRAN model
Merged Met Office radar data and quality controlled rain gauge data.
Met Office radar data.
Gridded quality controlled rain gauge data (IF Environment Agency rain gauge data exists).
File structure
Data inputs format
\inputs - root inputs data folder
Data outputs format
\outputs - root outputs data folder
\SHETRAN - SHETRAN rainfall input data, which should be in the correct format to run the model if running at 15 minute resolution (Note: We somehow need to add start date and data resolution into the library shetran set-up file I think).
\HIPIMS - HIPIMS rainfall input data, which should be in the correct format to run the model at 15 minute resolution
Data minimum requirements
Minimum data requirement to run model
Either Met Office C-band radar data, or Environment Agency rain gauge data.

SHETRAN 1 and 2

Requirements:
\input\MET exists and contains the files arrays.npy, timestamp.csv, coords_x.csv and coords_y.csv
Additional information if available:
\input\EA\15min exists and contains any .csv files
\input\UO\15min exists and contains any .csv files
\input\CS\15min exists and contains any .csv files
\input\NGIF\15min exists and contains any .csv files
SHETRAN 3

Requirements:
\input\EA\15min exists and contains more than one .csv file
Additional information if available:
\input\UO\15min exists and contains any .csv files
\input\CS\15min exists and contains any .csv files
\input\NGIF\15min exists and contains any .csv files
HIPIMS 1

Requirements:
\input\UO\radar\15min exists and contains the files arrays.npy, timestamp.csv, coords_x.csv and coords_y.csv
\input\MET exists and contains the files arrays.npy, timestamp.csv, coords_x.csv and coords_y.csv
Additional information if available:
\input\EA\15min exists and contains any .csv files
\input\UO\15min exists and contains any .csv files
\input\CS\15min exists and contains any .csv files
\input\NGIF\15min exists and contains any .csv files
HIPIMS 2

Requirements:
\input\UO\radar\15min exists and contains the files arrays.npy, timestamp.csv, coords_x.csv and coords_y.csv
\input\MET exists and contains the files arrays.npy, timestamp.csv, coords_x.csv and coords_y.csv
Additional information if available:
\input\EA\15min exists and contains any .csv files
\input\UO\15min exists and contains any .csv files
\input\CS\15min exists and contains any .csv files
\input\NGIF\15min exists and contains any .csv files

### Project Team
Amy Green, Newcastle University  ([amy.green3@newcastle.ac.uk](mailto:amy.green3@newcastle.ac.uk))  
Elizabeth Lewis, Newcastle University  ([elizabeth.lewis2@newcastle.ac.uk](mailto:elizabeth.lewis2@newcastle.ac.uk))  

### RSE Contact
Robin Wardle  
RSE Team, Newcastle Data  
Newcastle University NE1 7RU  
([robin.wardle@newcastle.ac.uk](mailto:robin.wardle@newcastle.ac.uk))  

## Built With

[Python 3](https://www.python.org)  

[Docker](https://www.docker.com)  

Other required tools: [tar](https://www.unix.com/man-page/linux/1/tar/), [zip](https://www.unix.com/man-page/linux/1/gzip/).

## Getting Started

### Prerequisites
TBC

### Installation
TBC

### Running Locally
TBC

### Running Tests
TBC

## Deployment

### Local
A local Docker container that mounts the test data can be built and executed using:

```
docker build . -t pyramid-prepare-data
docker run -v "$(pwd)/data:/data" pyramid-prepare-data
```

Note that output from the container, placed in the `./data` subdirectory, will have `root` ownership as a result of the way in which Docker's access permissions work.

### Production
#### DAFNI upload
The model is containerised using Docker, and the image is _tar_'ed and _zip_'ed for uploading to DAFNI. Use the following commands in a *nix shell to accomplish this.

```
docker build . -t pyramid-prepare-data
docker save -o pyramid-read-external-dummy.tar pyramid-prepare-data:latest
gzip pyramid-prepare-data.tar
```

The `pyramid-prepare-data.tar.gz` Docker image and accompanying DAFNI model definintion file (`model-definition.yml`) can be uploaded as a new model using the "Add model" facility at [https://facility.secure.dafni.rl.ac.uk/models/](https://facility.secure.dafni.rl.ac.uk/models/).

## Usage
The deployed model can be run in a DAFNI workflow. See the [DAFNI workflow documentation](https://docs.secure.dafni.rl.ac.uk/docs/how-to/how-to-create-a-workflow) for details.


## Roadmap
- [x] Initial Research  
- [ ] Minimum viable product <-- You are Here  
- [ ] Alpha Release  
- [ ] Feature-Complete Release  

## Contributing
TBD

### Main Branch
All development can take place on the main branch. 

## License
This code is private to the PYRAMID project.

## Acknowledgements
This work was funded by NERC, grant ref. NE/V00378X/1, “PYRAMID: Platform for dYnamic, hyper-resolution, near-real time flood Risk AssessMent Integrating repurposed and novel Data sources”. See the project funding [URL](https://gtr.ukri.org/projects?ref=NE/V00378X/1).
