import ee
import os
import json
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

from scraper import authenticate, load_province_boundaries, reduce_image, process_province
   
def main():
    authenticate()
    
    boundaries_path = os.path.join(os.getcwd(), "boundaries", "simplified", "simplified_philippines_province_boundaries.json")
    temporary_output_path = os.path.join(os.getcwd(), "scraped_data", "precipitation-temporary")
    output_folder = os.path.join(os.getcwd(), "scraped_data", "precipitation")
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(temporary_output_path, exist_ok=True)
    
    province_boundaries = load_province_boundaries(path=boundaries_path)
    
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2020, 3, 1)
    date_step = timedelta(days=50)
    scale = 55500
    collection_name = 'NOAA/CPC/Precipitation'
    band_name = 'precipitation'
    
    df = pd.DataFrame()
    
    for province, boundary in province_boundaries.items():
        province_df = process_province(province=province,
                                       boundary=boundary, 
                                       start_date=start_date, 
                                       end_date=end_date,
                                       date_step=date_step,
                                       scale=scale, 
                                       collection_name=collection_name, 
                                       band_name=band_name, 
                                       temporary_output_path=temporary_output_path)
        
        if province_df is not None:
            df = province_df if df.empty else df.merge(province_df, on="date", how="outer")
    
    
    
    csv_filename = "precipitation_per_province.csv"
    csv_path = os.path.join(output_folder, csv_filename)
    df.to_csv(csv_path, index=False)
    print(f"Saved: {csv_path}")

if __name__ == "__main__":
    main()
