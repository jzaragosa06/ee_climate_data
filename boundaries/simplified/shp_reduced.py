import geopandas as gpd
import os
from pathlib import Path

# Load shapefile
root_dir = os.getcwd()
filename = "gadm41_PHL_1.shp"
shapefile_path = os.path.join(root_dir, "..", "ph_shapefile", filename)
gdf = gpd.read_file(shapefile_path)

# Define a simplification tolerance
tolerance = 0.01  # Adjust this for more/less simplification

# Apply simplification
gdf["geometry"] = gdf["geometry"].simplify(tolerance, preserve_topology=True)

# Save the new simplified shapefile
simplified_shapefile_path = os.path.join(root_dir, "simplified_philippines_provinces.shp")
gdf.to_file(simplified_shapefile_path)

print(f"Simplified shapefile saved at: {simplified_shapefile_path}")
