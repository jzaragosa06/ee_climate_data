import geopandas as gpd
import json
import os
from pathlib import Path

# Load shapefile
root_dir = os.getcwd()
filename = "gadm41_PHL_1.shp"
shapefile_path = os.path.join(root_dir, "..", "ph_shapefile", filename)
print(shapefile_path)

gdf = gpd.read_file(shapefile_path)




# Define a simplification tolerance (adjust for more/less detail)
tolerance = 0.01  # Increase this value for more simplification

# Convert to GeoJSON format
province_boundaries = {}

for _, row in gdf.iterrows():
    province_name = row["NAME_1"]  # Adjust column name if necessary
    geometry = row["geometry"]  # Province boundary geometry
    
    # Simplify the geometry
    simplified_geometry = geometry.simplify(tolerance, preserve_topology=True)

    # Extract coordinates
    if simplified_geometry.geom_type == "Polygon":
        coordinates = [list(simplified_geometry.exterior.coords)]
    elif simplified_geometry.geom_type == "MultiPolygon":
        coordinates = [list(p.exterior.coords) for p in simplified_geometry.geoms]
    else:
        continue  # Skip non-polygon geometries
    
    province_boundaries[province_name] = coordinates

# Save to JSON file
output_json = "simplified_philippines_province_boundaries.json"
with open(output_json, "w") as f:
    json.dump(province_boundaries, f, indent=4)

print(f"Simplified province boundaries saved to {output_json}")
