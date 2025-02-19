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
output_folder = os.path.join(os.getcwd(), "scraped_data")

os.makedirs(output_folder, exist_ok=True)

# open json file containing the boundaries
with open(boundaries_path, "r") as file:
    province_boundaries = json.load(file)

start_date = datetime(2008, 1, 1)
end_date = datetime(2025, 2, 1)
date_step = timedelta(days=180)
collection_name = 'NOAA/CPC/Precipitation'
band_name = 'precipitation'
resolution = 55500  # in meters

def extract_data(image):
    date = ee.Date(image.get('system:time_start')).format('YYYY-MM-dd')
    mean_value = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=resolution,
        bestEffort=True
    ).get(band_name)
    return ee.Feature(None, {'date': date, 'precipitation': mean_value})

df = pd.DataFrame()

# Loop through each province
for province, boundary in province_boundaries.items():
    try:
        print(f"Processing {province}...")
        
        # boundaries of province. extracted from shapefile
        geometry = ee.Geometry.Polygon(boundary)

        all_data = []
        current_start = start_date
        
        while current_start < end_date:
            # prevents overflow
            current_end = min(current_start + date_step, end_date)
            print(f"Fetching data from {current_start.date()} to {current_end.date()} for {province}")
            
            rainfall = ee.ImageCollection(collection_name).filterDate(
                current_start.strftime('%Y-%m-%d'), current_end.strftime('%Y-%m-%d')
            ).select(band_name)
            
            rainfall_data = rainfall.map(extract_data).getInfo()
            
            
            for feature in rainfall_data['features']:
                date = feature['properties']['date']
                precipitation = feature['properties']['precipitation']
                all_data.append([date, precipitation])
                
            current_start = current_end

        province_name = province.replace(" ", "_") 
        province_df = pd.DataFrame(all_data, columns=['date', province_name])

        if df.empty:
            df = province_df
        else:
            df = df.merge(province_df, on="date", how="outer")
            
        csv_filename = f"temporary_last_{province}.csv"
        csv_path = os.path.join(output_folder, csv_filename)
        df.to_csv(csv_path, index=False)
    except Exception as e:
        print(f"failed to extract: {province}")
    else:
        pass

# Save locally as CSV
csv_filename = "precipitation_per_province_v2.csv"
csv_path = os.path.join(output_folder, csv_filename)
df.to_csv(csv_path, index=False)
print(f"Saved: {csv_path}")
    
    

