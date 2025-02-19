# Extracting Climatic Historical data

Extracting climatic variables from Google Earth Engine using Python API

## Setup

1. Fork this the repository.
2. Navigate to the folder.
3. on the terminal, run the following:

```
pip install -r requirements.txt
```

4. Create a project on Google Earth Engine
5. Authenticate on your computer by running the `authenticate.py`.

| ![Image 1](/public/NOAA_CPC_Precipitation_sample.png) | ![Image 2](/public/MODIS_061_MOD11A1_sample.png) |
| ----------------------------------------------------- | ------------------------------------------------ |

## Datasource

<table>
  <tr>
    <th>Climatic Variable</th>
    <th>Source Title</th>
    <th>DataSet Provider</th>
    <th>Dataset Availability</th>
    <th>Band(s)</th>
    <th>Pixel size</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Precipitation</td>
    <td><a href = "https://developers.google.com/earth-engine/datasets/catalog/NOAA_CPC_Precipitation#bands">CPC Global Unified Gauge-Based Analysis of Daily Precipitation</a></td>
    <td><a href ="https://psl.noaa.gov/data/gridded/data.cpc.globalprecip.html">NOAA Physical Sciences Laboratory</td>
    <td>2006-01-01T00:00:00Z–2025-02-14T00:00:00Z</td>
    <td>precipitation</td>
    <td>55500 meters</td>
    <td>
    The CPC Unified Gauge-Based Analysis of Global Daily Precipitation dataset offers daily precipitation estimates over land from 1979 to the present. Developed by NOAA's Climate Prediction Center (CPC), it leverages an optimal interpolation technique to combine data from a global network of rain gauges, with over 30,000 gauges contributing to the retrospective version (1979-2005) and around 17,000 to the real-time version (2006-present). Data is provided at a 0.5-degree resolution and includes both precipitation amounts (in 0.1 mm) and the number of gauges used for each grid cell, allowing users to assess data quality. The dataset's quality is acknowledged to be poor over tropical Africa and Antarctica, and generally varies with gauge density. Real-time data is subject to revision as more complete station data becomes available. This folder has all the technical documentation.The historical data spanning from 1979 to 2005 is not available in the current version of the dataset.
    </td>
  </tr>

  <tr>
    <td>Land Surface Temperature (LST)</td>
    <td><a href = "https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD11A1#bands">MOD11A1.061 Terra Land Surface Temperature and Emissivity Daily Global 1km</a></td>
    <td><a href ="https://lpdaac.usgs.gov/products/mod11a1v061/">NASA LP DAAC at the USGS EROS Center</td>
    <td>2000-02-24T00:00:00Z–2025-02-12T00:00:00Z</td>
    <td>LST_Day_1km (scale: 0.02, offset: None), LST_Night_1km (scale: 0.02, offset: None) </td>
    <td>1000 meters</td>
    <td>
    The MOD11A1 V6.1 product provides daily land surface temperature (LST) and emissivity values in a 1200 x 1200 kilometer grid. The temperature value is derived from the MOD11_L2 swath product. Above 30 degrees latitude, some pixels may have multiple observations where the criteria for clear-sky are met. When this occurs, the pixel value is the average of all qualifying observations. Provided along with both the day-time and night-time surface temperature bands and their quality indicator layers are MODIS bands 31 and 32 and six observation layers.
    </td>
  </tr>
</table>
