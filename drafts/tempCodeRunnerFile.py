
# # Convert to GeoJSON format
# province_boundaries = {}

# for _, row in gdf.iterrows():
#     province_name = row["Province"]  # Adjust column name based on your data
#     geometry = row["geometry"]  # Province boundary geometry
    
#     # Extract coordinates
#     if geometry.geom_type == "Polygon":
#         coordinates = [list(geometry.exterior.coords)]
#     elif geometry.geom_type == "MultiPolygon":
#         coordinates = [list(p.exterior.coords) for p in geometry.geoms]
#     else:
#         continue  # Skip non-polygon geometries
    
#     province_boundaries[province_name] = coordinates

# # Save to JSON file
# output_json = "philippines_province_boundaries.json"
# with open(output_json, "w") as f:
#     json.dump(province_boundaries, f, indent=4)

# print(f"Province boundaries saved to {output_json}")
