import ee
import os
import json
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

ee.Authenticate()
projectName = os.getenv("PROJECT")
ee.Initialize(project=projectName)


lst = ee.ImageCollection('MODIS/061/MOD11A1')

# Initial date of interest (inclusive).
i_date = '2022-01-01'

# Final date of interest (exclusive).
f_date = '2023-01-01'

# Selection of appropriate bands and dates for LST.
band = lst.select('LST_Day_1km', 'QC_Day').filterDate(i_date, f_date)

Hamburg_lon = 9.993682
Hamburg_lat = 53.551086
Hamburg_point = ee.Geometry.Point(Hamburg_lon, Hamburg_lat)


scale = 1000  # scale in meters

lst_Hamburg_full = band.getRegion(Hamburg_point, scale).getInfo()
lst_Hamburg_full[:3] # Preview the output.


import pandas as pd
df = pd.DataFrame(lst_Hamburg_full) #Convert list to dataframe
headers = df.iloc[0]   # Rearrange the header.
df = pd.DataFrame(df.values[1:], columns=headers)   # Rearrange the header.
df = df[['longitude', 'latitude', 'time', "LST_Day_1km" ]].dropna() # Remove rows with null data.
df[ "LST_Day_1km"] = pd.to_numeric(df[ "LST_Day_1km"], errors='coerce')    # Convert to numeric values.
df['datetime'] = pd.to_datetime(df['time'], unit='ms')  # Convert datetime to datetime values.
df = df[['time','datetime',  "LST_Day_1km"   ]] # take interest part
df.head()

def kelvin_to_celcius(t_kelvin):
    t_celsius =  t_kelvin*0.02 - 273.15
    return t_celsius
df['LST_Day_1km'] = df['LST_Day_1km'].apply(kelvin_to_celcius)
df.head()