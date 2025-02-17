var geometry =
    /* color: #d63000 */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-102.0115234375, 40.045027965879555],
        [-102.0115234375, 37.09085497132735],
        [-94.584765625, 37.09085497132735],
        [-94.584765625, 40.045027965879555]]], null, false);


//Define area
var aoi = geometry

//Define start & end Date
var startDate = '2011-01-01'
var endDate = '2012-01-01'

//Define rainfall data

//CHIRPS daily (mm/day): UCSB-CHG/CHIRPS/DAILY, precipitation, 5000
//TRMM 3-Hourly (mm/day): TRMM/3B42, precipitation, 27000
//ERA daily (m/day): ECMWF/ERA5/DAILY, total_precipitation, 27830

var imageCollection = 'NOAA/CPC/Precipitation'
var bandName = 'precipitation'
var resolution = 55500     //in meters


////////////////////////////////
var rainfall = ee.ImageCollection(imageCollection)
    .filter(ee.Filter.date(startDate, endDate))
    .select(bandName);

var chart = ui.Chart.image.series({
    imageCollection: rainfall,
    region: aoi,
    reducer: ee.Reducer.mean(),
    scale: resolution,
});
print(chart);

Map.addLayer(aoi)
Map.centerObject(aoi)  