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

boundaries_path = os.path.join(os.getcwd(), "boundaries", "simplified", "simplified_philippines_province_boundaries.json")
temporary_output_folder = os.path.join(os.getcwd(), "scraped_data", "temporary_folder_lst")
output_folder = os.path.join(os.getcwd(), "scraped_data", "lst")
os.makedirs(output_folder, exist_ok=True)

with open(boundaries_path, "r") as file:
    province_boundaries = json.load(file)

i_date = '2022-01-01'
f_date = '2022-01-10'
scale = 1000
collection_name = 'MODIS/061/MOD11A1'

lst = ee.ImageCollection(collection_name)
# Selection of appropriate bands and dates for LST.
band = lst.select('LST_Day_1km', 'QC_Day').filterDate(i_date, f_date)

for province, boundary in province_boundaries.items():
    try:
        print(f"processing...{province}")
        geometry = ee.Geometry.Polygon(boundary)
        lst_full = band.getRegion(geometry, scale).getInfo()
        
        df = pd.DataFrame(lst_full) #Convert list to dataframe
        headers = df.iloc[0]   # Rearrange the header.
        df = pd.DataFrame(df.values[1:], columns=headers)   # Rearrange the header.
        df = df[['longitude', 'latitude', 'time', "LST_Day_1km" ]].dropna() # Remove rows with null data.
        df[ "LST_Day_1km"] = pd.to_numeric(df[ "LST_Day_1km"], errors='coerce')    # Convert to numeric values.
        df['datetime'] = pd.to_datetime(df['time'], unit='ms')  # Convert datetime to datetime values.
        df = df[['time','datetime',  "LST_Day_1km"   ]] # take interest part
        
        csv_filename = f"lst_{province}.csv"
        csv_path = os.path.join(temporary_output_folder, csv_filename)
        df.to_csv(csv_path, index=False)
        print(f"{province} saved")
    except Exception as e:
        print(f"error: {e}")

    
    