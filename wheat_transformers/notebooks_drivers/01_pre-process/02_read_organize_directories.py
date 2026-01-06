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
# data_base = "/Users/hn/Documents/01_research_data/Ehsan/wheat/Data/"
# Define the base directory relative to your current working directory
dir_base = "./../../../01_research_data/Ehsan/wheat/"
data_base = dir_base + "Data/"
raw_dir = os.path.join(data_base, "00_raw_by_location/")
# raw_dir = os.path.abspath(raw_dir)

# %%
fullName_units = pd.read_csv(data_base + "inputs_column_names_v1.csv")
fullName_units

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
sorted(df.columns)

# %%
sorted(all_files.columns)

# %%
sorted(all_files.location.unique())[:5]

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
# Create a dictionary with 'variable_short' as the key and 'variable_name' as the value
variable_dict = fullName_units.set_index('variable_short')['variable_name'].to_dict()
variable_dict = {key.lower(): value for key, value in variable_dict.items()}

# %%
# A = all_files.copy()
# # Display the dictionary
# A.columns = A.columns.str.lower()
# A.rename(columns=variable_dict, inplace=True)
# sorted(A.columns)

# %%
# Display the dictionary
all_files.columns = all_files.columns.str.lower()
all_files.rename(columns=variable_dict, inplace=True)

# %%
all_files.head(3)

# %% [markdown]
# ### Read add varieties

# %%
# %%time
planting_harvest_dates = pd.read_excel(data_base + "planting_harvest_dates.xlsx")
varieties_traits = pd.read_excel(data_base + "varieties_traits.xlsx")
planting_harvest_dates.rename(columns=lambda x: x.lower().replace(' ', '_'), inplace=True)

planting_harvest_dates["location"] = \
          planting_harvest_dates["location"].str.replace(". ", "_").str.replace(" ", "_").str.lower()
planting_harvest_dates.head(2)

# %%
planting_harvest_dates[(planting_harvest_dates["location"] == "walla_walla") & \
                       (planting_harvest_dates["year"] == 2001)]["planting_date"].unique()

# %%
planting_harvest_dates[(planting_harvest_dates["location"] == "farmington") & \
                       (planting_harvest_dates["year"] == 2002)]

# %%
varieties_traits.rename(columns=lambda x: x.lower().replace(' ', '_'), inplace=True)

varieties_traits.rename(columns={'irrigationstatus': 'irrigation_status'}, inplace=True)

varieties_traits["location"] = \
          varieties_traits["location"].str.replace(". ", "_").str.replace(" ", "_").str.lower()

varieties_traits.head(3)

# %%
# Move location to the beginning of dataframe.
all_files = all_files[["location", *all_files.columns.drop("location")]]
all_files.head(2)

# %%
varieties_traits["irrigation_status"].unique()

# %%
varieties_traits.groupby(["irrigation_status"]).count()

# %%
varieties_traits.groupby(["irrigation_status"]).size()

# %%
varieties_traits["grain_yield"].isna().sum() 

# %%
varieties_traits[varieties_traits.irrigation_status=="irrigated"].location.unique()

# %%
dryland_locs = list(varieties_traits[varieties_traits.irrigation_status=="dryland"].location.unique())
irrigated_locs = list(varieties_traits[varieties_traits.irrigation_status=="irrigated"].location.unique())

# %%
print([x for x in dryland_locs if ( x in irrigated_locs)])
print([x for x in irrigated_locs if ( x in dryland_locs)])

# %%
varieties_traits = varieties_traits[varieties_traits.irrigation_status=="dryland"].copy()
varieties_traits.reset_index(drop=True, inplace=True)
varieties_traits.head(3)
varieties_traits["irrigation_status"].unique()

# planting_harvest_dates.head(2)

# %%
sorted(dryland_locs)[:5]

# %%
sorted(irrigated_locs)[:5]

# %%
# Move location to the beginning of dataframe.
varieties_traits.insert(0, "location", varieties_traits.pop("location"))
varieties_traits.head(2)

# %% [markdown]
# ## Filter all_files and plant_dates: keep dryland only

# %%

# %%
# it appears weather data is available only for dryland
# as irrigated does not need them!
print (all_files.shape)
all_files = all_files[all_files.location.isin(varieties_traits["location"].unique())].copy()
print (all_files.shape)

# %%
all_files['date'][0]

# %%
all_files['date'] = pd.to_datetime(all_files['date'])
all_files["year"] = all_files['date'].dt.year
all_files.head(2)

# %%

# %%
sorted(planting_harvest_dates.location.unique())[:5]

# %%
sorted(all_files.location.unique())[:5]

# %%
# Pick drylands only
print (planting_harvest_dates.shape)
planting_harvest_dates = planting_harvest_dates[\
                                        planting_harvest_dates.location.isin(\
                                                            varieties_traits["location"].unique())].copy()
print (planting_harvest_dates.shape)

# %%
varieties_traits.head(2)

# %%
all_files.head(2)

# %%
planting_harvest_dates.head(2)

# %%
all_files.head(2)

# %%
all_files = pd.merge(all_files,
                     planting_harvest_dates[['year', 'location', 'planting_date', 'harvest_date']],
                     how="left", on=["location", "year"])

all_files.head(2)

# %%
planting_harvest_dates.head(2)

# %%
all_files[(all_files["location"]=="farmington") & (all_files["year"]==2002)].head(5)

# %%

# %%
# We cannot do common years since we want preseason/pre-plant data:

# common_index = (all_files.set_index(["location", "year"]).index
#                 .intersection(planting_harvest_dates.set_index(["location", "year"]).index)
#                 .intersection(df3.set_index(["location", "year"]).index)
#                )

# common =  all_files.merge(planting_harvest_dates[['year', 'location', 'planting date', 'harvest date']], 
#                           on=["location", "year"], how="inner")

# %%
filename = raw_dir + "raw_all_locations_all_time_scales.sav"

export_ = {"wheat_all_locs_raw": all_files,
           "varieties_traits" : varieties_traits,
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
sorted(all_files.columns)

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
filename = raw_dir + "raw_all_locations_separate_daily_monthly_fiveDay.sav"

export_ = {"wheat_all_locs_raw_daily": daily_df,
           "wheat_all_locs_raw_monthly": monthly_data,
           "wheat_all_locs_raw_fiveDay": five_day_data,
           "varieties_traits":varieties_traits,
           "source_code": "read_organize_directories",
           "Author": "HN",
           "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           "Note": "read and merged all files into 1 and changed column names for consistency"
          }

pickle.dump(export_, open(filename, 'wb'))

# %%
