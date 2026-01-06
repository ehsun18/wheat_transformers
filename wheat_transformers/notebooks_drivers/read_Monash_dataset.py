# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: wheat_transformers
#     language: python
#     name: wheat_transformers
# ---

# %%
import sys
import os
import pandas as pd

# %%
cond_ = False
a = 1
counter = 0
while a > 0.5:
    a *= (365-counter)/365
    counter+=1

# %%

# %%

# %%
os.getcwd()

# %%
sys.path.append("./../mv_transformer/src")
import datasets.utils as datasets_utils

import importlib;
importlib.reload(datasets_utils);

# %%
ehsan_dir = "./../../../01_research_data/Ehsan/"

data_base = ehsan_dir + "wheat/Data/"
raw_dir = os.path.join(data_base, "00_raw_by_location/")

monarsh_data = ehsan_dir + "Monarsh_Regresshion_Archive/"

# %%
os.path.abspath(raw_dir)

# %%
file_path = monarsh_data + "BeijingPM10Quality/BeijingPM10Quality_TRAIN.ts"
with open(file_path, "r") as file:
    content = file.read()

# %%

# %%
BeijingPM10_TRAIN_df = datasets_utils.load_from_tsfile_to_dataframe(full_file_path_and_name=file_path,
                                                                    return_separate_X_and_y=True,
                                                                    replace_missing_vals_with="NaN")

# %%
BeijingPM10_X = BeijingPM10_TRAIN_df[0]
BeijingPM10_y = BeijingPM10_TRAIN_df[1]

# %%
BeijingPM10_X.shape

# %%
BeijingPM10_X.head(3)

# %%
BeijingPM10_X.tail(3)

# %%
(BeijingPM10_X.loc[10, "dim_1"])

# %%
type((BeijingPM10_X.loc[10, "dim_1"]))

# %%
BeijingPM10_X.loc[10, "dim_1"].index

# %%

# %%
type(BeijingPM10_X.loc[200, "dim_4"])

# %%
BeijingPM10_X.shape

# %%
for row in range(BeijingPM10_X.shape[0]):
    for col in BeijingPM10_X.columns:
        if BeijingPM10_X.loc[row, col].isna().any().any():
            print (f"{row, col}")

# %%
BeijingPM10_X.loc[3, 'dim_2']

# %%

# %%
file_name = "raw_all_locations_separate_daily_monthly_fiveDay.sav"
raw_example = pd.read_pickle(raw_dir + file_name)
raw_example.keys()

# %%
wheat_all_locs_raw_daily = raw_example["wheat_all_locs_raw_daily"]
wheat_all_locs_raw_daily.head(2)

# %%
list(wheat_all_locs_raw_daily.columns)

# %%
