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

# %% [markdown]
# In this notebook we can create aggregation configuration files to write on the disk.
#
# Later we can organize these better.
#
# Lets get going first
#
# - Dec. 29, 2025
# - HN

# %%
import os
import configparser
from datetime import datetime

dir_base = "./../../../01_research_data/Ehsan/wheat/"
data_base = dir_base + "Data/"
raw_dir = os.path.join(data_base, "00_raw_by_location/")

config_dir = dir_base + "/configs/"
os.makedirs(config_dir, exist_ok=True)

# %%
config = configparser.ConfigParser()

# preserve capitals, otherwise, everything will be lower case
config.optionxform = str

# %%
Scenario_1_aggr_cols = {
    "avg_rh_perc": "mean",
    "avg_temp_c": "mean",
    "cum_gdd_cday": "sum",
    "dailyGDD_diff_cday": "mean",
    "dap": "mean",
    "diurnal_temp_range_c": "mean",
    "freezing_dd_cday": "mean",
    "heat_dd_cday": "mean",
    "max_rh_perc": "mean",
    "max_temp_c": "mean",
    "min_rh_perc": "mean",
    "min_temp_c": "mean",
    "potential_evapo_mmday": "mean",
    "precip_dtr_mmdayc": "mean",
    "precip_mmday": "sum",
    "specific_humidity_kgkg": "mean",
    "sr_wm2": "mean",
    "vpd_kpa": "mean",
    "wet_day_frequency_days": "mean",
    "wind_speed_ms" : "mean"
}

Scenario_1_meta_data = {
    "Author": "HN",
    "Notebook": "create_aggregation_config_files",
    "Note": "Aggregate daily data into 5-day resolution. Scenario 1",
    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}

Scenario_1_config_dict = {
    "parameters": Scenario_1_aggr_cols,
    "metadata": Scenario_1_meta_data,
}

# %%
for section, params in Scenario_1_config_dict.items():
    config[section] = {k: str(v) for k, v in params.items()}

file_path = config_dir + "Scenario_1_aggr_cols.cfg"

with open(file_path, "w") as configfile:
    config.write(configfile)

# %%
dir_base

# %%
