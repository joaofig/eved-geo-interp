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

# Running the Code

The code base consists of three Python scripts that must be executed in order.

## Sample Collection
This script determines the nine reference temperature sources.
It then collects 2700 sample observations from the original dataset for IDW parameter validation.
Each of these samples gets queried against the source Open-Meteo temperature provider, and the resulting temperature is used as a ground truth.
The script ends by saving the samples to the `samples.csv` file in the data folder.

```shell
python collect-samples.py
```

## IDW Power Parameter Tuner
After collecting the samples, we can now tune the IDW power parameter using the collected ground truth temperatures.

```shell
python tune-idw-power.py
```

This script generates temperature interpolations by varying the IDW power parameter from 1 to 10 and storing the resulting RMSE values in the `data/out/power_tune.csv` file.

## Updating Temperatures
The final script computes the temperature interpolation using the optimum power parameter for the whole dataset.
This script creates new versions of the original input files in the output data folder.

```shell
python update-temperatures.py
```
