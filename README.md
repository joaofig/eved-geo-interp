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

For **Windows** or manual users, follow these steps:

1. Clone the data repository using the following command:
```
git clone https://bitbucket.org/datarepo/eved_dataset.git
```
2. Extract the files in the `eVED.gz` archive. 
3. Copy the `eVED` folder to the `data` folder of the present project tree. 
4. Delete the cloned folder (`eved_dataset`). 
5. Open the `eVED_180124_week.csv` file on a text editor and remove all instances of the colon character (`;`). 
6. Save the file.
