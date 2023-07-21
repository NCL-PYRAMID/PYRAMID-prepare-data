# PYRAMID Prepare Data

## About
Reads data from the "read-external" model step and prepares this for feeding into SHETRAN.

Prepares data to go into SHETRAN and HIPIMS
### Notes
This code relies on the following code
- `read_met-office` - reads in 5-minute gridded (composite and processed C-band weather radar from the Met Office ftp server.
- `read_ea` - reads in 15-minute rain gauge data from the EA website API.
- `read_cs` - reads in varying resolution rain gauge data from NGIF and UO APIand accumulates up to 15-minute resolution data.
- `read_cs_radar - reads in Urban Observatory X-band radar code, processes it and accumulates it up to 15 minutes.
- `intense_qc` - quality controls all gauge data using intense-qc code (Note: this is designed for hourly rain gauge data).

It also requires the bounding box shapefile for HIPIMS and the Tyne mask file for SHETRAN (these are in the `static.zip` file - see below).

### What does this code do?
#### Reads in data
1. Read in radar data (if exists)
    - Met Office radar data
    - Urban Observatory radar data
2. Read in quality controlled rain gauge data (if exists)
    - Environment Agency rain gauges
    - Urban Observatory rain gauges
    - Citizen Science rain gauges
    - National Green Infrastructure Facility rain gauges
3. Identifies best data to use
    - Uses data priority for HIPIMS
    - Uses data priority for SHETRAN
4. Grids/merges data
    - Combines different data types to provide gridded 15-minute rainfall estimates (1km resolution)
5. Saves data in correct format for models
    - Clips and saves data in correct format for HIPIMS
    - Clips and saves data in correct format for SHETRAN

#### Prioritises data for input into HIPIMS model
1. High resolution (250m) X-band radar data, merged with rain gauges, which is conditional on Met Office C-band radar data.
2. High resolution (250m) X-band radar data, conditional on Met Office C-band radar data.
3. High resolution (250m) X-band radar data, merged with rain gauges.
4. Merged Met Office radar data and quality controlled rain gauge data.
5. Met Office radar data.
6. Gridded quality controlled rain gauge data (IF Environment Agency rain gauge data exists).

NOTE: 1. and 2. are missing as cannot test this whilst the Urban Observatory radar is down for maintenence and API is not working.

#### Prioritises data for input into SHETRAN model
1. Merged Met Office radar data and quality controlled rain gauge data.
2. Met Office radar data.
3. Gridded quality controlled rain gauge data (IF Environment Agency rain gauge data exists).

### File structure
#### Data inputs format
`\inputs` - root inputs data folder

#### Data outputs format
- `\outputs` - root outputs data folder
    - `\SHETRAN` - SHETRAN rainfall input data, which should be in the correct format to run the model if running at 15 minute resolution (Note: We somehow need to add start date and data resolution into the library shetran set-up file I think).
    - `\HIPIMS` - HIPIMS rainfall input data, which should be in the correct format to run the model at 15 minute resolution

### Data minimum requirements
#### Minimum data requirement to run model
Either Met Office C-band radar data, or Environment Agency rain gauge data.

- SHETRAN 1 and 2
    1. Requirements:
        - `inputs\MET` exists and contains the files `arrays.npy`, `timestamp.csv`, `coords_x.csv` and `coords_y.csv`
    2. Additional information if available:
        - `inputs\EA\15min` exists and contains any `.csv` files
        - `inputs\UO\15min` exists and contains any `.csv` files
        - `inputs\CS\15min` exists and contains any `.csv` files
        - `inputs\NGIF\15min` exists and contains any `.csv` files

- SHETRAN 3
    1. Requirements:
        - `inputs\EA\15min` exists and contains more than one `.csv` file
    2. Additional information if available:
        - `inputs\UO\15min` exists and contains any `.csv` files
        - `inputs\CS\15min` exists and contains any `.csv` files
        - `inputs\NGIF\15min` exists and contains any `.csv` files

- HIPIMS 1
    1. Requirements:
        - `inputs\UO\radar\15min` exists and contains the files `arrays.npy`, `timestamp.csv`, `coords_x.csv` and `coords_y.csv`
    - `inputs\MET` exists and contains the files `arrays.npy`, `timestamp.csv`, `coords_x.csv` and `coords_y.csv`
    2. Additional information if available:
        - `inputs\EA\15min` exists and contains any `.csv` files
        - `inputs\UO\15min` exists and contains any `.csv` files
        - `inputs\CS\15min` exists and contains any `.csv` files
        - `inputs\NGIF\15min` exists and contains any `.csv` files

- HIPIMS 2
    1. Requirements:
        - `inputs\UO\radar\15min` exists and contains the files `arrays.npy`, `timestamp.csv`, `coords_x.csv` and `coords_y.csv`
        - `inputs\MET` exists and contains the files `arrays.npy`, `timestamp.csv`, `coords_x.csv` and `coords_y.csv`
    2. Additional information if available:
        - `inputs\EA\15min` exists and contains any `.csv` files
        - `inputs\UO\15min` exists and contains any `.csv` files
        - `input\CS\15min` exists and contains any `.csv` files
        - `inputs\NGIF\15min` exists and contains any `.csv` files

### Project Team
Amy Green, Newcastle University  ([amy.green3@newcastle.ac.uk](mailto:amy.green3@newcastle.ac.uk))  
Elizabeth Lewis, Newcastle University  ([elizabeth.lewis2@newcastle.ac.uk](mailto:elizabeth.lewis2@newcastle.ac.uk))  

### RSE Contact
Robin Wardle  
RSE Team, Newcastle Data  
Newcastle University NE1 7RU  
([robin.wardle@newcastle.ac.uk](mailto:robin.wardle@newcastle.ac.uk))  

## Built With
[Python 3](https://www.python.org); [Docker](https://www.docker.com); [Anaconda](https://www.anaconda.com/)

Other required tools: [tar](https://www.unix.com/man-page/linux/1/tar/), [zip](https://www.unix.com/man-page/linux/1/gzip/).

## Getting Started

### Prerequisites
Python 3.9 is required to run the Python script, and Docker also needs to be installed. If working on a Windows system, it is recommended that WSL is used for any local Docker builds; a) because DAFNI requires Linux Docker images, and b) native command-line Linux tools are much superior to those provided by Windows.

An up-to-date version of Anaconda must be installed.

### Installation
The models are Python 3 scripts and need no installation for local execution. Deployment to DAFNI is covered below.

### Running Locally
The model can be run in a `bash` shell in the repository directory.

```
conda create -f environment.yml
conda activate prepare-data
jupyter nbconvert --to python prepare-data.ipynb
python -u prepare-data.py
```

The model will require some data to generate meaningful outputs. Refer to the [read-met-office](https://github.com/NCL-PYRAMID/PYRAMID-read-met-office) and [read-ea](https://github.com/NCL-PYRAMID/PYRAMID-read-ea) model repositories for instructions on using these models to extract data from the Met Office and Environment Agency APIs. Input data should be placed in the `./data/inputs` subdirectory.

### Running Tests
There are no additional tests at present.

## Deployment

### Local
A local Docker container that mounts the test data can be built and executed using:

```
docker build . -t pyramid-prepare-data -f Dockerfile
docker run -v "$(pwd)/data:/data" pyramid-prepare-data
```

Note that output from the container, placed in the `./data` subdirectory, will have `root` ownership as a result of the way in which Docker's access permissions work.

### Production
#### DAFNI upload
The model is containerised using Docker, and the image is _tar_'ed and _zip_'ed for uploading to DAFNI. Use the following commands in a *nix shell to accomplish this.

```
docker build . -t pyramid-prepare-data -f Dockerfile
docker save -o pyramid-prepare-data.tar pyramid-prepare-data:latest
gzip pyramid-prepare-data.tar
```

The `pyramid-prepare-data.tar.gz` Docker image and accompanying DAFNI model definintion file (`model-definition.yml`) can be uploaded as a new model using the "Add model" facility at [https://facility.secure.dafni.rl.ac.uk/models/](https://facility.secure.dafni.rl.ac.uk/models/). Alternatively, the existing model can be updated manually in DAFNI by locating the relevant model through the DAFNI UI, selecting "Edit Model", uploading a new image and / or metadata file, and incrementing the semantic version number in the "Version Message" field appropriately.

As of 20/07/2023 the SHETRAN DAFNI parent model UUID is `a51af454-4501-4ae8-bfee-8a4ece535671`.

#### CI/CD with GitHub Actions
The `prepare-data`` model can be deployed to DAFNi using GitHub Actions. The relevant workflows are built into the model repository and use the DAFNI Model Uploader Action to update the DAFNI model. The workflows trigger on the creation of a new release tag which follows semantic versioning and takes the format vx.y.z where x is a major release, y a minor release, and z a patch release.

As DAFNI is in development, occasionally the API will be updated necessitating a new Model Uploader release. Before creating a new tagged release, check the status of the DAFNI Model Uploader at https://github.com/dafnifacility/dafni-model-uploader, updating the version in the [upload action](https://github.com/NCL-PYRAMID/PYRAMID-prepare-data/blob/main/.github/workflows/upload.yml) if necessary before creating a new model release.

The DAFNI model upload process is prone to failing, often during model ingestion, in which case a deployment action will show a failed status. Such deployment failures might be a result of a DAFNI timeout, or there might be a problem with the model build. It is possible to re-run the action in GitHub if it is evident that the failure is as a result of a DAFNI timeout. However, deployment failures caused by programming errors (e.g. an error in the model definition file) that are fixed as part of the deployment process will not be included in the tagged release! It is thus best practice in case of a deployment failure always to delete the version tag and to go through the release process again, re-creating the version tag and re-triggering the workflows.

The DAFNI model upload process requires valid user credentials. These are stored in the NCL-PYRAMID organization "Actions secrets and variables", and are:
```
DAFNI_SERVICE_ACCOUNT_USERNAME
DAFNI_SERVICE_ACCOUNT_PASSWORD
```
Any NCL-PYRAMID member with a valid DAFNI login may update these credentials.

## Usage
The deployed model can be run in a DAFNI workflow. See the [DAFNI workflow documentation](https://docs.secure.dafni.rl.ac.uk/docs/how-to/how-to-create-a-workflow) for details.


## Roadmap
- [x] Initial Research  
- [x] Minimum viable product  <-- You are Here  
- [ ] Alpha Release  
- [ ] Feature-Complete Release  

## Contributing
The `prepare-data` for DAFNI project has ended. Pull requests from outside the project team will be ignored.

### Main Branch
The stable branch is `main`. All development should take place on new branches. Pull requests are enabled on `main`.

## License
TBC

## Acknowledgements
This work was funded by NERC, grant ref. NE/V00378X/1, “PYRAMID: Platform for dYnamic, hyper-resolution, near-real time flood Risk AssessMent Integrating repurposed and novel Data sources”. See the project funding [URL](https://gtr.ukri.org/projects?ref=NE/V00378X/1).
