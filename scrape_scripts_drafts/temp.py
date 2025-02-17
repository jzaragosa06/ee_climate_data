import os
import json

# boundaries_path = os.path.join(os.getcwd(), "..", "boundaries","philippines_province_boundaries.json")
boundaries_path = os.path.join(os.getcwd(), "..", "boundaries","simplified", "simplified_philippines_province_boundaries.json")



with open(boundaries_path, "r") as file:
    boundaries = json.load(file)
    
print(boundaries)