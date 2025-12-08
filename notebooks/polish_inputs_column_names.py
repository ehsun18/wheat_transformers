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
import pandas as pd
import os

# %%
# data_base = "/Users/hn/Documents/01_research_data/Ehsan/wheat/Data/"
# Define the base directory relative to your current working directory
data_base = "./../../../01_research_data/Ehsan/wheat/Data/"
raw_dir = os.path.join(data_base, "00_raw_by_location/")
# raw_dir = os.path.abspath(raw_dir)

# %%

# %%
fullName_units = pd.read_csv(data_base + "inputs_column_names.csv")
fullName_units.head(3)
fullName_units.rename(columns=lambda x: x.lower().replace(' ', '_'), inplace=True)
fullName_units["variable_name"] = fullName_units["variable_name"].str.lower() + "_" +\
                                  fullName_units["unit"].str.lower()


fullName_units["variable_name"] = fullName_units["variable_name"].str.replace(' ', '_')
fullName_units['variable_name'] = fullName_units['variable_name'].str.replace('maximum', 'max', case=False)
fullName_units['variable_name'] = fullName_units['variable_name'].str.replace('minimum', 'min', case=False)
fullName_units['variable_name'] = fullName_units['variable_name'].str.replace('minimum', 'min', case=False)


a = 'standardize_precipitation_evapotranspiration_index_unitless'
b = 'std_precip_evap_unitless'
fullName_units['variable_name'] = fullName_units['variable_name'].str.replace(a, b, case=False)

a = 'absolute_difference_in_gdd_between_two_adjacent_days_cday'
b = 'dailyGDD_diff_cday'
fullName_units['variable_name'] = fullName_units['variable_name'].str.replace(a, b, case=False)


a = 'palmer_drought_severity_index_unitless'
b = 'palmer_drought_unitless'
fullName_units['variable_name'] = fullName_units['variable_name'].str.replace(a, b, case=False)


fullName_units['variable_name'] = fullName_units['variable_name'].str.replace("temperature", "temp", case=False)

fullName_units['variable_name'] = fullName_units['variable_name'].str.replace("evapotranspiration", 
                                                                              "evapo", case=False)


fullName_units['variable_name'] = fullName_units['variable_name'].str.replace("cumulative", 
                                                                              "cum", case=False)

fullName_units['variable_name'] = fullName_units['variable_name'].str.replace("growing_degree_days", 
                                                                              "gdd", case=False)

fullName_units['variable_name'] = fullName_units['variable_name'].str.replace("%", 
                                                                              "perc", case=False)

fullName_units['variable_name'] = fullName_units['variable_name'].str.replace("percentage", 
                                                                              "perc", case=False)

fullName_units['variable_name'] = fullName_units['variable_name'].str.replace("precentage", 
                                                                              "perc", case=False)

fullName_units['variable_name'] = fullName_units['variable_name'].str.replace("relative_humidity", 
                                                                              "rh", case=False)

fullName_units['variable_name'] = fullName_units['variable_name'].str.replace("degree_days", 
                                                                              "dd", case=False)

fullName_units['variable_name'] = fullName_units['variable_name'].str.replace("october", 
                                                                              "oct", case=False)


fullName_units['variable_name'] = fullName_units['variable_name'].str.replace("average", 
                                                                              "avg", case=False)

fullName_units['variable_name'] = fullName_units['variable_name'].str.replace("precipitation", 
                                                                              "precip", case=False)

fullName_units['variable_name'] = fullName_units['variable_name'].str.replace("solar_radiation", 
                                                                              "sr", case=False)

fullName_units['variable_name'] = fullName_units['variable_name'].str.replace("vapor_pressure_deficit", 
                                                                              "vpd", case=False)


fullName_units['variable_short'] = fullName_units['variable_short'].str.replace("WDF", 
                                                                                "WD", case=False)

fullName_units.head(2)

# %%
fullName_units.to_csv(data_base + "inputs_column_names_v1.csv", index=False)

# %%
fullName_units['variable_short'].str.contains('WDF').sum()

# %%
