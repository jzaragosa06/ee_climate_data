import ee
# Trigger the authentication flow.
ee.Authenticate()

# Initialize the library.
ee.Initialize(project='ee-zukozaragosa2003')



# Define AOI
geometry = ee.Geometry.Polygon(
    [[[-102.0115234375, 40.045027965879555],
      [-102.0115234375, 37.09085497132735],
      [-94.584765625, 37.09085497132735],
      [-94.584765625, 40.045027965879555]]])

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
print(rainfall_data)

# Export to Google Drive
# task = ee.batch.Export.table.toDrive(
#     collection=rainfall_data,
#     description='Rainfall_Data_Export',
#     fileFormat='CSV',
#     folder='EarthEngineExports'
# )

# # Start the task automatically
# task.start()
# print("Export task started successfully!")
