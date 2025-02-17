import ee
# Trigger the authentication flow.
ee.Authenticate()

# Initialize the library.
ee.Initialize(project='ee-zukozaragosa2003')

# Define AOI
geometry = ee.Geometry.Polygon([[[120.29625115806084, 16.04828714904824],
          [120.29625115806084, 15.826442458884308],
          [120.53383050376397, 15.826442458884308],
          [120.53383050376397, 16.04828714904824]]])

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
task = ee.batch.Export.table.toDrive(
    collection=rainfall_data,
    description='dagupan',
    fileFormat='CSV',
    folder='EarthEngineExports'
)

# Start the task automatically
task.start()
print("Export task started successfully!")
