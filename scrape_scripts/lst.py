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
os.makedirs(temporary_output_folder, exist_ok=True)

with open(boundaries_path, "r") as file:
    province_boundaries = json.load(file)

i_date = '2022-01-01'
f_date = '2022-01-10'
scale = 1000
collection_name = 'MODIS/061/MOD11A1'
band_name = 'LST_Day_1km'

lst = ee.ImageCollection(collection_name).select(band_name, 'QC_Day').filterDate(i_date, f_date)


def reduce_image(image, geometry):
    date = ee.Date(image.get('system:time_start')).format('YYYY-MM-dd')
    mean_lst = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=scale,
        bestEffort=True
    ).get(band_name)
    return ee.Feature(None, {'date': date, band_name: mean_lst})

for province, boundary in province_boundaries.items():
    try:
        print(f"processing...{province}")
        
        geometry = ee.Geometry.Polygon(boundary)
        
        time_series = lst.map(lambda img: reduce_image(image=img, geometry=geometry)).filter(ee.Filter.notNull([band_name]))
        
        df = pd.DataFrame(time_series.getInfo()['features'])
        df = pd.json_normalize(df['properties'])
        df[band_name] = df[band_name] * 0.02 - 273.15
    
        
        csv_filename = f"lst_{province}.csv"
        csv_path = os.path.join(output_folder, csv_filename)
        df.to_csv(csv_path, index=False)
        print(f"{province} saved")
    except Exception as e:
        print(f"error: {e}")

    
    