import pandas as pd
from typing import List, Optional, Any
import transformersCores.config as cfg
import numpy as np


def aggregate_per5day(
    params: "cfg.aggregateParameters", daily_df: pd.DataFrame, fiveDay_df: pd.DataFrame
) -> pd.DataFrame:
    """Return aggregated variables by converting daily variables to 5-day aggregations
    to match the variables that are recorded evert 5 day


    Arguments
    ---------
    s : params
       parameters object

    daily_df : panda dataframe

    fiveDay_df : panda dataframe

    Returns
    -------
    agg_daily_5day : panda dataframe
      aggregated daily data to 5-day resolution

    """
    daily_df["date"] = pd.to_datetime(daily_df["date"])
    fiveDay_df["date"] = pd.to_datetime(fiveDay_df["date"])

    daily_df.sort_values(["location", "date"], inplace=True)
    fiveDay_df.sort_values(["location", "date"], inplace=True)

    daily_df.reset_index(drop=True, inplace=True)
    fiveDay_df.reset_index(drop=True, inplace=True)

    params = vars(params)
    agg_cols = [col for col in params.keys() if col in daily_df.columns]
    agg_dict = {col: params[col] for col in agg_cols}

    ### the following 2 lines are hard coded. perhaps put it in config object?
    categorical_vars_list = ["final_season", "season", "stage"]
    # we can get planting date and harvest date later and merge them
    unique_per_group_vars = ["planting_date", "harvest_date"]

    # Add categorical columns to keep (pick first)
    for col in categorical_vars_list:
        if col in daily_df.columns:
            agg_dict[col] = "first"

    # Add unique-per-group columns (assert unique)
    for col in unique_per_group_vars:
        if col in daily_df.columns:
            agg_dict[col] = lambda x: x.unique()[0]

    five_day_dates = fiveDay_df["date"].values

    # Assign the 5-day date
    # Create a new column for the assigned 5-day date
    daily_df["five_day_date"] = pd.NaT

    # Process each location separately
    for loc in daily_df["location"].unique():
        # Dates for this location in 5-day data, sorted
        five_day_dates_loc = (
            fiveDay_df.loc[fiveDay_df["location"] == loc, "date"].sort_values().values
        )

        # Mask for daily rows of this location
        mask = daily_df["location"] == loc
        daily_dates_loc = daily_df.loc[mask, "date"].values

        # Assign the next 5-day date >= daily date
        indices = np.searchsorted(five_day_dates_loc, daily_dates_loc, side="left")

        # Some daily dates might be after the last 5-day date -> set to NaT
        indices[indices >= len(five_day_dates_loc)] = -1

        assigned_dates = np.array(
            [pd.NaT if i == -1 else five_day_dates_loc[i] for i in indices]
        )
        daily_df.loc[mask, "five_day_date"] = assigned_dates

    # Group and aggregate
    agg_daily_5day = (
        daily_df.groupby(["location", "five_day_date"]).agg(agg_dict).reset_index()
    )

    # rename columns to reflect the operation we did:
    agg_rules = {
        col: params[col] for col in params if col in daily_converted_2_5day.columns
    }
    rename_dict = {col: f"{agg}_{col}" for col, agg in agg_rules.items()}

    # Rename the columns
    daily_converted_2_5day = daily_converted_2_5day.rename(columns=rename_dict)

    daily_converted_2_5day.rename(columns={"five_day_date": "date"}, inplace=True)
    return agg_daily_5day
