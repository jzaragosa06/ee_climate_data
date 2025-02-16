import ee
import os
import json
import pandas as pd
from datetime import datetime

# Authenticate & Initialize
ee.Authenticate()
ee.Initialize(project='ee-zukozaragosa2003')

# Paths
boundaries_path = os.path.join(os.getcwd(), "boundaries", "simplified", "simplified_philippines_province_boundaries.json")
output_folder = os.path.join(os.getcwd(), "rainfall_data")  # Local folder to save CSVs

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)

# Load province boundaries
with open(boundaries_path, "r") as file:
    province_boundaries = json.load(file)

# Define parameters
start_date = '2011-01-01'
end_date = '2012-01-01'
collection_name = 'NOAA/CPC/Precipitation'
band_name = 'precipitation'
resolution = 55500  # in meters


# Extract data function
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

        # Define AOI
        geometry = ee.Geometry.Polygon(boundary)

        # Get rainfall data
        rainfall = ee.ImageCollection(collection_name).filterDate(start_date, end_date).select(band_name)

        # Convert to FeatureCollection
        rainfall_data = rainfall.map(extract_data).getInfo()

        # Convert GEE response to pandas DataFrame
        data = []
        date = None
        precipitation = None
        for feature in rainfall_data['features']:
            date = feature['properties']['date']
            precipitation = feature['properties']['precipitation']


        if "date" not in df.columns:
            df["date"] = date
            df[f"{province.replace(" ", "_")}"] = precipitation
        else:
            df[f"{province.replace(" ", "_")}"] = precipitation
        pass
    except Exception as e:
        print(f"failed to extract: {province}")
        pass
    else:
        pass

# Save locally as CSV
csv_filename = "precipitation_all_province.csv"
csv_path = os.path.join(output_folder, csv_filename)
df.to_csv(csv_path, index=False)
print(f"Saved: {csv_path}")
    
    

