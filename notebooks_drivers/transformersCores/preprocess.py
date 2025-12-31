import pandas as pd
from typing import List, Optional, Any
import transformersCores.config as cfg
import numpy as np


def TS_df_countMonths_prior2Plant(df: pd.DataFrame, months_prior: int) -> pd.DataFrame:
    """
    For each location & planting_date, collect numeric columns as pd.Series
    from `months_prior` months before planting_date (aligned to month start)
    through harvest_date.

    months_prior says, for example, 3 months before plant date.
    The difference between this function and TS_df_givenMonth_prior2Plant()
    is that in this function we say start 3 months prior to plant date,
    in TS_df_givenMonth_prior2Plant() we say start Oct. of the year prior to lant date

    if plant date is 2002-04-16, then time series would
    start from 2002-01-01: beginning of 3 months before planting date.

    Arguments:
    -----------
    df : pd.DataFrame
        Must contain 'location', 'date', 'planting_date', 'harvest_date' columns.

    start_month : int
        Month (1-12) to start the window in the year preceding planting date.

    Returns:
    --------
    pd.DataFrame
        One row per location & planting_date.
        Columns: location, planting_date, harvest_date, numeric columns...
        Each numeric column cell contains a pd.Series.
    """

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["planting_date"] = pd.to_datetime(df["planting_date"])
    df["harvest_date"] = pd.to_datetime(df["harvest_date"])

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    rows = []

    for (loc, planting), group in df.groupby(["location", "planting_date"]):
        harvest = group["harvest_date"].iloc[0]

        # Compute start date: X months before planting, aligned to month start
        start = (planting - pd.DateOffset(months=months_prior)).replace(day=1)

        # Filter ALL data for this location
        loc_data = df[df["location"] == loc]
        filtered = loc_data[(loc_data["date"] >= start) & (loc_data["date"] <= harvest)]

        series_dict = {col: filtered.set_index("date")[col] for col in numeric_cols}

        series_dict.update(
            {"location": loc, "planting_date": planting, "harvest_date": harvest}
        )

        rows.append(series_dict)

    final_df = pd.DataFrame(rows)

    cols_order = ["location", "planting_date", "harvest_date"] + numeric_cols
    final_df = final_df[cols_order]

    return final_df


def TS_df_givenMonth_prior2Plant(
    df: pd.DataFrame, start_month: int = 10
) -> pd.DataFrame:
    """
    For each location and planting_date, collect all numeric columns
    in a window from start_month preceding the planting_date until harvest_date.
    Each cell contains a pd.Series indexed by 'date'.

    Arguments:
    -----------
    df : pd.DataFrame
        Must contain 'location', 'date', 'planting_date', 'harvest_date' columns.
    start_month : int
        Month (1-12) to start the window in the year preceding planting date.

    Returns:
    --------
    pd.DataFrame
        One row per location & planting_date.
        Columns: location, planting_date, harvest_date, numeric columns...
        Each numeric column cell contains a pd.Series.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["planting_date"] = pd.to_datetime(df["planting_date"])
    df["harvest_date"] = pd.to_datetime(df["harvest_date"])

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    # Prepare a list to collect results
    rows = []

    # Iterate by location and planting date (but filter from all location's data)
    for (loc, planting), group in df.groupby(["location", "planting_date"]):
        harvest = group["harvest_date"].iloc[0]
        start = pd.Timestamp(year=planting.year - 1, month=start_month, day=1)

        # Filter **all data from the location** in the desired window
        loc_data = df[df["location"] == loc]
        filtered = loc_data[(loc_data["date"] >= start) & (loc_data["date"] <= harvest)]

        # Build dictionary of Series per numeric column
        series_dict = {col: filtered.set_index("date")[col] for col in numeric_cols}
        series_dict["harvest_date"] = harvest

        # Add location and planting_date
        series_dict["location"] = loc
        series_dict["planting_date"] = planting

        rows.append(series_dict)

    # Convert list of dicts into DataFrame
    final_df = pd.DataFrame(rows)

    # Reorder columns: location, planting_date, harvest_date, numeric columns
    cols_order = ["location", "planting_date", "harvest_date"] + numeric_cols
    final_df = final_df[cols_order]

    return final_df


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
    daily_df = daily_df.copy()
    fiveDay_df = fiveDay_df.copy()

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
    agg_rules = {col: params[col] for col in params if col in agg_daily_5day.columns}
    rename_dict = {col: f"{agg}_{col}" for col, agg in agg_rules.items()}

    # Rename the columns
    agg_daily_5day = agg_daily_5day.rename(columns=rename_dict)

    agg_daily_5day.rename(columns={"five_day_date": "date"}, inplace=True)
    return agg_daily_5day
