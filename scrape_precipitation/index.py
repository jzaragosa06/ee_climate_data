import ee
# Trigger the authentication flow.
ee.Authenticate()

# Initialize the library.
ee.Initialize(project='ee-zukozaragosa2003')

# json file containing the coordinates
import os
import json

# run this on root
boundaries_path = os.path.join(os.getcwd(), "boundaries", "simplified",  "simplified_philippines_province_boundaries.json")
with open (boundaries_path, "r") as file:
    province_boundaries = json.load(file)
    

for province, boundary in province_boundaries.items():
    # Define AOI
    geometry = ee.Geometry.Polygon(boundary)

    # Define parameters
    start_date = '2011-01-01'
    end_date = '2012-01-01'
    collection_name = 'NOAA/CPC/Precipitation'
    band_name = 'precipitation'
    resolution = 55500  # in meters

    # Get rainfall data
    rainfall = ee.ImageCollection(collection_name).filterDate(start_date, end_date).select(band_name)

    # Function to extract mean precipitation for each image
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
    rainfall_data = rainfall.map(extract_data)

    # Export to Google Drive
    task = ee.batch.Export.table.toDrive(
        collection=rainfall_data,
        description=f"{province}",
        fileFormat='CSV',
        folder='precipitation_per_province'
    )

    # Start the task automatically
    task.start()
    print(f"{province} - Export task started successfully!")
