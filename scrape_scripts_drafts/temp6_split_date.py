import ee
import os
import json
import pandas as pd
from datetime import datetime, timedelta

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
start_date = datetime(2008, 1, 1)
end_date = datetime(2025, 2, 1)
date_step = timedelta(days=180)  # Split into 180-day chunks
collection_name = 'NOAA/CPC/Precipitation'
band_name = 'precipitation'
resolution = 55500  # in meters

# Loop through each province
for province, boundary in province_boundaries.items():
    try:
        print(f"Processing {province}...")

        # Define AOI
        geometry = ee.Geometry.Polygon(boundary)

        all_data = []
        current_start = start_date

        while current_start < end_date:
            current_end = min(current_start + date_step, end_date)
            print(f"Fetching data from {current_start.date()} to {current_end.date()} for {province}...")

            # Get rainfall data
            rainfall = ee.ImageCollection(collection_name).filterDate(
                current_start.strftime('%Y-%m-%d'), current_end.strftime('%Y-%m-%d')
            ).select(band_name)

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

            # Convert to FeatureCollection
            rainfall_data = rainfall.map(extract_data).getInfo()

            # Convert GEE response to pandas DataFrame
            for feature in rainfall_data['features']:
                date = feature['properties']['date']
                precipitation = feature['properties']['precipitation']
                all_data.append([date, precipitation])

            # Move to the next time chunk
            current_start = current_end

        # Convert collected data to DataFrame
        df = pd.DataFrame(all_data, columns=['date', 'precipitation'])

        # Save locally as CSV
        csv_filename = f"{province.replace(' ', '_')}.csv"
        csv_path = os.path.join(output_folder, csv_filename)
        df.to_csv(csv_path, index=False)
        print(f"Saved: {csv_path}")
    except Exception as e:
        print(f"Failed: {province}. Error: {e}")
