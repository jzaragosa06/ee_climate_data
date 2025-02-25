# this function modularize the existing codes for reusabiity
import ee
import os
import json
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

def authenticate():
    ee.Authenticate()
    projectName = os.getenv("PROJECT")
    ee.Initialize(project=projectName)
    
# path to json path (i.e., boundaries json)
def load_province_boundaries(path):
    with open(path, "r") as file:
        return json.load(file)
    

def reduce_image(image, geometry, scale, band_name):
    date = ee.Date(image.get('system:time_start')).format('YYYY-MM-dd')
    mean = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=scale,
        bestEffort=True
    ).get(band_name)
    return ee.Feature(None, {'date': date, band_name: mean})

def process_province(province, boundary, start_date, end_date, date_step, scale, collection_name, band_name, temporary_output_path):
    try:
        print(f"processing {province} ...")
        geometry = ee.Geometry.Polygon(boundary)
        
        current_start = start_date
        
        province_df = pd.DataFrame()
        while current_start < end_date:
            current_end = min(current_start + date_step, end_date)
            print(f"Fetching data from {current_start.date()} to {current_end.date()} for {province}")

            #image collection filtered already by collection name and band
            image_collection = ee.ImageCollection(collection_name).filterDate(
                current_start.strftime('%Y-%m-%d'), current_end.strftime('%Y-%m-%d')
            ).select(band_name)

            time_series = image_collection.map(lambda img: reduce_image(image=img, geometry=geometry, scale=scale, band_name=band_name))
            df_temp = pd.DataFrame(time_series.getInfo()['features'])
            df_temp = pd.json_normalize(df_temp['properties'])
            # df_temp[band_name] = df_temp[band_name] * 0.02 - 273.15
            
            province_df = df_temp if province_df.empty else pd.concat([province_df, df_temp], ignore_index=True)
            current_start = current_end
        
        csv_filename = f"lst_{province}.csv"
        csv_path = os.path.join(temporary_output_path, csv_filename)
        province_df.to_csv(csv_path, index=False)
        print(f"{province} saved")
        
        
        return province_df.rename(columns={band_name: province.replace(" ", "_") })
    except Exception as e:
        print(f"Error in processing {province}: {e}")
        return None
        
        