## Prerequisites
* [Python 3](https://www.python.org/downloads/)
* [pip](https://pypi.org/project/pip/)
## Setup <a name="setup"></a>
* Clone the repository
* Open the project folder in `Terminal`
* Run `pip install -r dependencies`
* This will install the following dependencies  
**requests, sklearn, numpy, pandas, matplotlib**
## Using the config
You can set multiple values in [config.ini](config.ini).

| Key                | Value                                                                                                                   |
| --------------     | ----------------------------------------------------------------------------------------------------------------------- |
| forecast_range     | An `int` value describing the forecast range in **days**                                                                |
| plot_history_range | An `int` value describing the amount of weather history visible in the output plot (Capped to history_range)
| history_range      | An `int` value describing the amount of days to retrieve from weather history                                           |
| attribute          | The attribute you want to predict. <br>See [Attributes](#attributes)                                                    |
| use_live_api       | Wether you want to use the most recent weather data or the dump provided in [assets/sampleData](assets/sampleData.json) |
| lat                | The latitude of the location you want to predict the weather at                                                         |
| lon                | The longitude of the location you want to predict the weather at                                                        |

## How to use <a name="tutorial"></a>
Make sure you have installed the dependencies from the [Setup](#setup) instructions before continuing.

* Open the project folder in `Terminal`
* Navigate to the software folder
* Run `python3 app.py`
## Attributes <a name="attributes"></a>
This is a list of all weather attributes this program is able to predict.  
If you edit the config variable `attribute` refer to the key column.

| Attribute           | Key               |
| ------------------- | ----------------- |
| Temperature         | `temperature`     |
| Maximum Temperature | `temperature_min` |
| Minimum Temperature | `temperature_max` |
| Precipitation       | `precipitation`   |
| Windspeed           | `windspeed`       |
| Peak Gust           | `peakgust`        |
| Pressure            | `pressure`        |
