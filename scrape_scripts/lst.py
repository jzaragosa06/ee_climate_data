import ee
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

from scraper import authenticate, load_province_boundaries, reduce_image, process_province
   
# this applies the scaling (refer to documentation)
# this converts the integer to float
def scale_value(x):
    return x * 0.02

def to_celcius(x):
    return x - 273.15


def main():
    authenticate()
    
    boundaries_path = os.path.join(os.getcwd(), "boundaries", "simplified", "simplified_philippines_province_boundaries.json")
    temporary_output_path = os.path.join(os.getcwd(), "scraped_data", "lst", "lst-temporary")
    output_folder = os.path.join(os.getcwd(), "scraped_data", "lst")
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(temporary_output_path, exist_ok=True)
    
    province_boundaries = load_province_boundaries(path=boundaries_path)
    
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2020, 3, 1)
    date_step = timedelta(days=50)
    scale = 1000
    collection_name = 'MODIS/061/MOD11A1'
    band_name = 'LST_Day_1km'
    
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
    
    # scale and to celcius
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].apply(scale_value)
    df[numeric_cols] = df[numeric_cols].apply(to_celcius)
    
    # arrange. ensure that date appear first
    df = df.reindex(columns=["date"] + [col for col in df.columns if col != "date"])
    
    csv_filename = "lst_per_province.csv"
    csv_path = os.path.join(output_folder, csv_filename)
    df.to_csv(csv_path, index=False)
    print(f"Saved: {csv_path}")

if __name__ == "__main__":
    main()
