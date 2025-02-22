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
temporary_output_folder = os.path.join(os.getcwd(), "scraped_data", "lst-temporary")

output_folder = os.path.join(os.getcwd(), "scraped_data", "lst")
os.makedirs(output_folder, exist_ok=True)
os.makedirs(temporary_output_folder, exist_ok=True)

with open(boundaries_path, "r") as file:
    province_boundaries = json.load(file)

start_date = datetime(2020, 1, 1)
end_date = datetime(2021, 1, 1)
date_step = timedelta(days=180)
scale = 1000
collection_name = 'MODIS/061/MOD11A1'
band_name = 'LST_Day_1km'

def reduce_image(image, geometry):
    date = ee.Date(image.get('system:time_start')).format('YYYY-MM-dd')
    mean_lst = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=scale,
        bestEffort=True
    ).get(band_name)
    return ee.Feature(None, {'date': date, band_name: mean_lst})

df = pd.DataFrame()

for province, boundary in province_boundaries.items():
    try:
        province_name = province.replace(" ", "_")
        
        print(f"processing...{province}")
        geometry = ee.Geometry.Polygon(boundary)
        current_start = start_date
        province_df = pd.DataFrame()    
        
        while current_start < end_date:
            current_end = min(current_start + date_step, end_date)
            print(f"Fetching data from {current_start.date()} to {current_end.date()} for {province}")

            lst = ee.ImageCollection(collection_name).filterDate(
                current_start.strftime('%Y-%m-%d'), current_end.strftime('%Y-%m-%d')
            ).select(band_name)

            time_series = lst.map(lambda img: reduce_image(image=img, geometry=geometry))
            df_temp = pd.DataFrame(time_series.getInfo()['features'])
            df_temp = pd.json_normalize(df_temp['properties'])
            df_temp[band_name] = df_temp[band_name] * 0.02 - 273.15
            
            if province_df.empty:
                province_df = df_temp
                
            else:
                province_df = pd.concat([province_df, df_temp], ignore_index=True)
        
            current_start = current_end
        
        #temporary save
        csv_filename = f"lst_{province}.csv"
        csv_path = os.path.join(temporary_output_folder, csv_filename)
        province_df.to_csv(csv_path, index=False)
        print(f"{province} saved")
        
        
        # save on just one df
        if df.empty:
            province_df = province_df.rename(columns={band_name: province_name})
            df = province_df
        else:
            province_df = province_df.rename(columns={band_name: province_name})
            df = df.merge(province_df, on="date", how="outer")

        #temporary save of last
        csv_filename = f"lst_-last-{province}.csv"
        csv_path = os.path.join(output_folder, csv_filename)
        df.to_csv(csv_path, index=False)
        print(f"last-{province} saved")
    except Exception as e:
        print(f"error: {e}")

csv_filename = f"lst_per_province_data_extracted_per_180days.csv"
csv_path = os.path.join(output_folder, csv_filename)
df.to_csv(csv_path, index=False)
print(f"saved: {csv_path}")

    
    