# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import warnings
warnings.filterwarnings("ignore")
from datetime import datetime
import pandas as pd
import numpy as np
import random
import os, os.path, pickle, sys

import matplotlib
import matplotlib.pyplot as plt

# %%
dpi_, map_dpi_ = 300, 300

# %%
os.getcwd()

# %%

# %%
# data_base = "/Users/hn/Documents/01_research_data/Ehsan/wheat/Data/"
# Define the base directory relative to your current working directory
data_base = "./../../../01_research_data/Ehsan/wheat/Data/"
raw_dir = os.path.join(data_base, "00_raw_by_location/")
# raw_dir = os.path.abspath(raw_dir)

# %%
fullName_units = pd.read_csv(data_base + "inputs_column_names_v1.csv")
fullName_units.head(2)

# %%

# %%
file_list = os.listdir(raw_dir)
file_list = [x for x in file_list if x.endswith("xlsx")]
file_list[:3]

# %%
df = pd.read_excel(raw_dir + file_list[0])
df.head(3)

# %%
### Check if all files share thew same columns

# %%
# %%time

no_cols = 0
check = True

for a_file in file_list:
    df = df = pd.read_excel(raw_dir + a_file)
    
    if no_cols == 0:
        no_cols = df.shape[1]
        columns_set = set(df.columns)
    else:
        if df.shape[1] != no_cols:
            print (f"{a_file} column count is different")
        
        if columns_set != set(df.columns):
            print (f"{a_file} has different columns")
            check = False
            
if check:
    all_files = pd.DataFrame()
    # Example: read all CSV files in a folder
    for a_file in file_list:
        df = pd.read_excel(raw_dir + a_file)
        df['location'] = a_file.replace(".xlsx", "").replace(". ", "_").replace(" ", "_").lower()
        all_files = pd.concat([all_files, df], ignore_index=True)


# %%
all_files.head(3)

# %%
fullName_units.shape

# %%
fullName_units.head(2)

# %%
fullName_units

# %%
# we do not need hour:minute:second:
all_files['date'] = pd.to_datetime(all_files['date']).apply(lambda x: x.date())
all_files.head(2)

# %%
fullName_units.sort_values(by='variable_short', inplace=True)
fullName_units.reset_index(drop=True, inplace=True)
fullName_units.head(2)

# %%
df = all_files.copy()

# %%

# %%
# Create a dictionary with 'variable_short' as the key and 'variable_name' as the value
variable_dict = fullName_units.set_index('variable_short')['variable_name'].to_dict()
variable_dict = {key.lower(): value for key, value in variable_dict.items()}
# Display the dictionary
all_files.columns = all_files.columns.str.lower()
all_files.rename(columns=variable_dict, inplace=True)

# %%
all_files.head(3)

# %%
df.head(3)

# %%
filename = raw_dir + "raw_all_locations_all_time_scales.sav"

export_ = {"wheat_all_locs_raw": all_files,
           "source_code": "read_organize_directories",
           "Author": "HN",
           "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           "Note": "read and merged all files into 1 and changed column names for consistency"
          }

pickle.dump(export_, open(filename, 'wb'))

# %%
monthly_cols = ["actual_evapo_mmmonth", "soil_moisture_mm"]
fiveDay_cols = ["std_precip_evap_unitless", "palmer_drought_unitless"]

# %%
all_files.head(2)

# %%

# %%
static_cols = ['date', 'doy', 'location']

# %%
monthly_data = all_files[static_cols + monthly_cols].copy()
monthly_data.dropna(inplace=True)
monthly_data.reset_index(drop=True, inplace=True)
monthly_data.head(3)

# %%
five_day_data = all_files[static_cols + fiveDay_cols].copy()
five_day_data.dropna(inplace=True)
five_day_data.reset_index(drop=True, inplace=True)
five_day_data.head(3)

# %%
daily_df = all_files.copy()
daily_df.drop(columns=monthly_cols + fiveDay_cols, inplace=True)
daily_df.head(3)

# %%
daily_df.shape

# %%
print(pd.__version__)

# %%
filename = raw_dir + "raw_all_locations_separate_daily_monthly_fiveDay.sav"

export_ = {"wheat_all_locs_raw_daily": daily_df,
           "wheat_all_locs_raw_monthly": monthly_data,
           "wheat_all_locs_raw_fiveDay": five_day_data,
           "source_code": "read_organize_directories",
           "Author": "HN",
           "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           "Note": "read and merged all files into 1 and changed column names for consistency"
          }

pickle.dump(export_, open(filename, 'wb'))

# %%
