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

# Loop through each province
for province, boundary in province_boundaries.items():
    print(f"Processing {province}...")

    # Define AOI
    geometry = ee.Geometry.Polygon(boundary)

    # Get rainfall data
    rainfall = ee.ImageCollection(collection_name).filterDate(start_date, end_date).select(band_name)

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
    data = []
    for feature in rainfall_data['features']:
        date = feature['properties']['date']
        precipitation = feature['properties']['precipitation']
        data.append([date, precipitation])

    df = pd.DataFrame(data, columns=['date', 'precipitation'])

    # Save locally as CSV
    csv_filename = f"{province.replace(' ', '_')}.csv"
    csv_path = os.path.join(output_folder, csv_filename)
    df.to_csv(csv_path, index=False)
    print(f"Saved: {csv_path}")

# (Optional) Upload all CSV files to Google Drive
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive

# # Authenticate Google Drive
# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()
# drive = GoogleDrive(gauth)

# # Upload each CSV file to Drive
# folder_id = 'YOUR_GOOGLE_DRIVE_FOLDER_ID'  # Replace with your Google Drive folder ID

# for file_name in os.listdir(output_folder):
#     file_path = os.path.join(output_folder, file_name)
#     gfile = drive.CreateFile({'title': file_name, 'parents': [{'id': folder_id}]})
#     gfile.SetContentFile(file_path)
#     gfile.Upload()
#     print(f"Uploaded: {file_name} to Google Drive")

# print("All province data successfully processed and uploaded.")
