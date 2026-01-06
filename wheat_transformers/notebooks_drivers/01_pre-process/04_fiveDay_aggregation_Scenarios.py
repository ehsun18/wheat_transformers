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

# %% [markdown]
# Let us agggregate data in 5-day intervals. That way we can use the variables whose temporal resolution are of 5-day granularity and also shortens the length of time series. It is likely(?) that we do not need track every thing on a daily basis.
#
# - Dec. 29, 2025
# - HN

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

from typing import List, Optional, Any

import configparser
import argparse

# from pathlib import Path
# PROJECT_ROOT = Path.cwd().parent
# sys.path.insert(0, str(PROJECT_ROOT))
# from transformersCores import config
# from transformersCores import config as cfg
import sys
sys.path.append('./../')
import transformersCores.config as cfg
import transformersCores.preprocess as prp

# %%

# %%
import importlib
importlib.reload(cfg);
importlib.reload(prp);

# %%
dir_base = "./../../../01_research_data/Ehsan/wheat/"
data_base = dir_base + "Data/"
raw_dir = os.path.join(data_base, "00_raw_by_location/")
configs_dir = dir_base + "configs/"

# %%
params = cfg.aggregateParameters()
params.readFromFile(configs_dir + "Scenario_1_aggr_cols.cfg")
# params = vars(params)

# %%
# params_v2 = cfg.aggregateParameters()
# params_v2.load_config_from_file(configs_dir + "Scenario_1_aggr_cols.cfg")

# %% [markdown]
# ### Read Data

# %%
filename = raw_dir + "raw_all_locations_separate_daily_monthly_fiveDay.sav"
data_dict = pd.read_pickle(filename)

# %%
data_dict.keys()

# %%
raw_daily = data_dict["wheat_all_locs_raw_daily"]
raw_fiveDay = data_dict["wheat_all_locs_raw_fiveDay"]
varieties_traits = data_dict["varieties_traits"]

# %%
raw_daily.head(2)

# %%

# %%
params = cfg.aggregateParameters()
params.readFromFile(configs_dir + "Scenario_1_aggr_cols.cfg")

daily_converted_2_5day = prp.aggregate_per5day(params=params, daily_df=raw_daily, fiveDay_df=raw_fiveDay)

# %%
raw_daily[(raw_daily["location"] == "walla_walla") & (raw_daily["year"] == 2003)].head(5)

# %%
raw_fiveDay[(raw_fiveDay["date"].dt.year == 2003) & (raw_fiveDay["location"] == "walla_walla")].head(5)

# %%
end_date = pd.to_datetime("2003-01-05")
loc = "walla_walla"
# end_date = raw_fiveDay["date"][0]
five_days = pd.date_range(end=end_date, periods=5, freq='D')
a_col = "precip_mmday"

raw_daily[(raw_daily["location"] == loc) & (raw_daily["date"].isin(five_days))][a_col].sum()

# %%
a_col = "sum_precip_mmday"
daily_converted_2_5day[(daily_converted_2_5day["location"] == loc) & \
                       (daily_converted_2_5day["date"] == end_date)][a_col]

# %%
daily_converted_2_5day.head(2)

# %%
raw_daily[(raw_daily["location"] == "walla_walla") & (raw_daily["year"] == 2001)]["planting_date"].unique()

# %%
daily_converted_2_5day['date'] = pd.to_datetime(daily_converted_2_5day['date'])
daily_converted_2_5day['planting_date'] = pd.to_datetime(daily_converted_2_5day['planting_date'])
daily_converted_2_5day['harvest_date'] = pd.to_datetime(daily_converted_2_5day['harvest_date'])

# %%
daily_converted_2_5day_backup = daily_converted_2_5day.copy()

# %%
daily_converted_2_5day = daily_converted_2_5day_backup.copy()

# %%
# daily_converted_2_5day.dropna(subset=['planting_date'], inplace=True)
# daily_converted_2_5day.sort_values(["location", "date"], inplace=True)
# daily_converted_2_5day.reset_index(drop=True, inplace=True)

# daily_converted_2_5day.head(3)

# %%
daily_converted_2_5day_backup.head(3)

# %%

# %%
super_df_oct = prp.TS_df_givenMonth_prior2Plant(daily_converted_2_5day_backup, start_month=10)

# %% [markdown]
# ## Check point

# %%
super_df_oct.head(3)

# %%
t2 = super_df_oct.loc[0, "harvest_date"]
t1 = super_df_oct.loc[0, "planting_date"]
t1 = pd.Timestamp(f"{t1.year - 1}-10-01")

days_between = (t2 - t1).days
days_between

# %%
daily_converted_2_5day[(daily_converted_2_5day["location"] == "almira") & \
                       (daily_converted_2_5day['date'].dt.year == 2002)].head(3)

# %%
locations_list = daily_converted_2_5day["location"].unique()
loc_ = locations_list[0]

loc_yr = daily_converted_2_5day.loc[daily_converted_2_5day["location"] == \
                                      loc_, "harvest_date"].unique()[-1]
loc_yr

# %%
test_super = super_df_oct[(super_df_oct["location"] == loc_) & (super_df_oct["harvest_date"] == loc_yr)]
test_super

# %%
start_date = pd.Timestamp(year=loc_yr.year - 1, month=10, day=1)

test_df = daily_converted_2_5day[(daily_converted_2_5day["location"] == loc_) & \
                                 (daily_converted_2_5day["date"] >= start_date) & \
                                 (daily_converted_2_5day["date"] <= loc_yr)]

# %%
a_col = "mean_dailyGDD_diff_cday"
sum(test_df[a_col].values - test_super[a_col].item().values)

# %% [markdown]
# ### Time series 3 months prior planting date as opposed to prior Oct.

# %%
import importlib
importlib.reload(cfg);
importlib.reload(prp);

# %%
super_df_3months = prp.TS_df_countMonths_prior2Plant(daily_converted_2_5day_backup, months_prior=3)

# %% [markdown]
# ## Check point

# %%
locations_list = daily_converted_2_5day["location"].unique()
loc_ = locations_list[0]

loc_yr = daily_converted_2_5day.loc[daily_converted_2_5day["location"] == \
                                      loc_, "planting_date"].unique()[2]
loc_yr

# %%
test_super = super_df_3months[(super_df_3months["location"] == loc_) & \
                              (super_df_3months["planting_date"] == loc_yr)]
test_super

# %%
three_months_prior = loc_yr - pd.DateOffset(months=3)
start_date = three_months_prior.replace(day=1)

harvest_date = daily_converted_2_5day.loc[(daily_converted_2_5day["location"] == loc_) & \
                           (daily_converted_2_5day["planting_date"] == loc_yr)]["harvest_date"].unique()[0]

test_df = daily_converted_2_5day[(daily_converted_2_5day["location"] == loc_) & \
                                 (daily_converted_2_5day["date"] >= start_date) & \
                                 (daily_converted_2_5day["date"] <= harvest_date)]
test_df.head(3)

# %%
a_col = "mean_dap"
sum(test_df[a_col].values - test_super[a_col].item().values)

# %%
