import pyreadr
import pandas as pd
import numpy as np

def load_and_process_data(file_path: str, dataset: str) -> pd.DataFrame:
    """
    Loads R data from the specified file path and performs initial processing.
    This includes type conversions and date parsing.

    Args:
        file_path (str): The path to the .rdata file.
        dataset (str): Specifies the name of the dataset in file.

    Returns:
        pd.DataFrame: A processed pandas DataFrame.
    """
    result = pyreadr.read_r(file_path)
    df = result[dataset]

    df["origin_census_block_group"] = df["origin_census_block_group"].astype(str)
    df["destination_cbg"] = df["destination_cbg"].astype(str)
    df["device_count"] = pd.to_numeric(df["device_count"], errors="coerce")
    df["destination_device_count"] = pd.to_numeric(df["destination_device_count"], errors="coerce")
    df["year"] = df["year"].astype(int)
    df["uid"] = df["uid"].astype(int)
    df["date"] = pd.to_datetime("2019-01-01") + pd.to_timedelta(df["uid"] - 1, unit="D") #
    
    return df

def filter_by_cbg(df: pd.DataFrame, cbg: str) -> pd.DataFrame:
    """
    Filters the DataFrame for a specific destination census block group (CBG).

    Args:
        df (pd.DataFrame): The input DataFrame.
        cbg (str): The destination census block group to filter by.

    Returns:
        pd.DataFrame: A DataFrame containing data only for the specified CBG.
    """
    return df[df['destination_cbg'] == cbg] #

def compute_indegree_by_destination(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes the sum of 'destination_device_count' as 'in_degree' grouped by 'destination_cbg' and 'date'.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A DataFrame with 'destination_cbg', 'date', and 'in_degree'.

    Raises:
        Exception: If the dataset contains data for more than one CBG.
    """
    if len(df['destination_cbg'].unique()) > 1:
        raise Exception("The Dataset has more than one CBG.")
    grouped_indegree_df = df.groupby(["destination_cbg", "date"])["destination_device_count"].sum().reset_index() #
    grouped_indegree_df.rename(columns={"destination_device_count": "in_degree"}, inplace=True) #
    return grouped_indegree_df

def smoothen_data(df: pd.DataFrame, smoothing_period: int = 7) -> pd.DataFrame:
    """
    Applies a rolling mean to the 'in_degree' column for smoothing.

    Args:
        df (pd.DataFrame): The input DataFrame with an 'in_degree' column.
        smoothing_period (int): The window size for the rolling mean.

    Returns:
        pd.DataFrame: A DataFrame with the smoothed 'in_degree' column.
    """
    df_smoothed = df.copy() #
    df_smoothed["in_degree"] = ( #
        df["in_degree"]
        .rolling(window=smoothing_period, center=True, min_periods=1)
        .mean()
    )
    df_smoothed["in_degree"] = ( #
        df_smoothed["in_degree"]
        .bfill()
        .ffill()
    )
    return df_smoothed

def calculate_baseline(df: pd.DataFrame, disaster_start: pd.Timestamp, baseline_days_to_average_before_disaster: int = 15) -> float:
    """
    Calculates the baseline 'in_degree' value by averaging data before the disaster start.

    Args:
        df (pd.DataFrame): The input DataFrame with 'date' and 'in_degree' columns.
        disaster_start (pd.Timestamp): The start date of the disaster.
        baseline_days_to_average_before_disaster (int): Number of days before disaster_start to include in the baseline calculation.

    Returns:
        float: The calculated baseline value.
    """
    baseline_start = disaster_start - pd.Timedelta(days=baseline_days_to_average_before_disaster)
    baseline_end = disaster_start - pd.Timedelta(days=1)

    baseline_df = df[ #
        (df["date"] >= baseline_start) &
        (df["date"] <= baseline_end)
    ]
    
    baseline_value = baseline_df["in_degree"].mean()
    return baseline_value

def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalizes the 'in_degree' column of the DataFrame to a 0-1 scale.

    Args:
        df (pd.DataFrame): The input DataFrame with an 'in_degree' column.

    Returns:
        pd.DataFrame: A DataFrame with the normalized 'in_degree' column.
    """
    df_normalized = df.copy() #
    min_val = df["in_degree"].min() #
    max_val = df["in_degree"].max() #
    if (max_val - min_val) == 0:
        df_normalized["in_degree"] = 0 # Avoid division by zero if all values are the same
    else:
        df_normalized["in_degree"] = (df_normalized["in_degree"] - min_val) / (max_val - min_val) #
    return df_normalized

def baseline_normalization(df: pd.DataFrame, baseline_value: float) -> pd.DataFrame:
    """
    Normalizes the 'in_degree' column based on a calculated baseline value.

    Args:
        df (pd.DataFrame): The input DataFrame with an 'in_degree' column.
        baseline_value (float): The baseline value to normalize against.

    Returns:
        pd.DataFrame: A DataFrame with the baseline-normalized 'in_degree' column.
    """
    df_normalized = df.copy() #
    if baseline_value == 0: #
        df_normalized['in_degree'] = np.nan #
    else:
        df_normalized['in_degree'] = (df_normalized['in_degree'] - baseline_value) / baseline_value #
    return df_normalized

def preprocess_data(df: pd.DataFrame, cbg: str, smoothing_period:int = 25) -> pd.DataFrame:
    """
    Preprocesses the df and make it ready for applying the resilience models.
    :param smoothing_period: period for smoothing the 'in_degree' column.
    :param df: input DataFrame
    :param cbg: cbg to filter the data upon
    :return: preprocessed DataFrame
    """
    df_filtered = filter_by_cbg(df, cbg)
    df_grouped = compute_indegree_by_destination(df_filtered)
    df_normalized = normalize_data(df_grouped)
    df_smoothed = smoothen_data(df_normalized, smoothing_period)
    return df_smoothed