# eved-geo-interp
Geospatial interpolation using the Extended Vehicle Energy Dataset

# Setup
Before ypu use the code in this repository, you must first set up the Python environment and download the source data.

## Code Setup
To set up your environment, run the following command:
```shell
make install
```
## Data Setup
To download and set up your data directory, run the following command:
```shell
make download-data
```
This command downloads the data from the official source repository and moves the data to the appropriate directory: `data/eVED`.