import pandas as pd
from typing import Tuple, Optional

from utils import get_relative_points, calculate_triangle_area, get_area_under_baseline, calculate_slope


def calculate_disaster_start_point(df: pd.DataFrame, disaster_start: pd.Timestamp) -> Tuple[pd.Timestamp, float]:
    """
    Calculates the point representing the start of the disaster (t0).

    Args:
        df (pd.DataFrame): The DataFrame with normalized 'in_degree' and 'date'.
        disaster_start (pd.Timestamp): The actual start date of the disaster.

    Returns:
        Tuple[pd.Timestamp, float]: A tuple (t0_date, t0_value).
    """

    t0_row = df[df["date"] == disaster_start]
    if t0_row.empty:
        t0_value = df.loc[df['date'].sub(disaster_start).abs().idxmin()]['in_degree']
        t0 = df.loc[df['date'].sub(disaster_start).abs().idxmin()]['date']
    else:
        t0 = disaster_start
        t0_value = t0_row["in_degree"].iloc[0]
    return t0, t0_value

def calculate_disaster_end_point(df: pd.DataFrame, disaster_end: pd.Timestamp) -> Tuple[pd.Timestamp, float]:
    """
    Calculates the point representing the end of the disaster.

    Args:
        df (pd.DataFrame): The DataFrame with normalized 'in_degree' and 'date'.
        disaster_end (pd.Timestamp): The actual end date of the disaster.

    Returns:
        Tuple[pd.Timestamp, float]: A tuple (inactive_date, inactive_value).
    """
    inactive_row = df[df["date"] == disaster_end]
    if inactive_row.empty:
        inactive_value = df.loc[df['date'].sub(disaster_end).abs().idxmin()]['in_degree']
        inactive = df.loc[df['date'].sub(disaster_end).abs().idxmin()]['date']
    else:
        inactive = disaster_end
        inactive_value = inactive_row["in_degree"].iloc[0]
    return inactive, inactive_value

def calculate_recovery_point(df_normalized: pd.DataFrame, disaster_end: pd.Timestamp, baseline_value: float) -> Tuple[Tuple[pd.Timestamp, float], bool]:
    """
    Calculates the recovery point (t1) or the new normal point if full recovery isn't achieved.

    Args:
        df_normalized (pd.DataFrame): The DataFrame with normalized 'in_degree' and 'date'.
        disaster_end (pd.Timestamp): The end date of the disaster.
        baseline_value (float): The calculated baseline 'in_degree' value.

    Returns:
        Tuple[Tuple[pd.Timestamp, float], bool]: A tuple containing:
            - (t1_date, t1_value) representing the recovery/new normal point.
            - A boolean indicating whether full recovery was achieved (True) or a new normal formed (False).
    """
    post_disaster_df = df_normalized[df_normalized["date"] >= disaster_end].copy()

    if post_disaster_df.empty:
        return (disaster_end, 0.0), False

    post_disaster_df = post_disaster_df.sort_values(by='date')

    recovery_df = post_disaster_df[post_disaster_df["in_degree"] >= baseline_value]

    if not recovery_df.empty:
        t1 = recovery_df["date"].iloc[0]
        t1_value = recovery_df["in_degree"].iloc[0]
        recover = True
    else:
        min_point = post_disaster_df["in_degree"].min()
        min_date = post_disaster_df[post_disaster_df["in_degree"] == min_point]["date"].iloc[0]
        tail_df = post_disaster_df[post_disaster_df["date"] >= min_date]
        
        if not tail_df.empty:
            t1_value = tail_df["in_degree"].max()
            t1 = tail_df[tail_df["in_degree"] == t1_value]["date"].iloc[0]
            if t1 == min_date:
                t1_value = baseline_value
        else:
            t1 = post_disaster_df['date'].iloc[-1] # Last available date
            t1_value = post_disaster_df['in_degree'].iloc[-1]
        recover = False

    return (t1, t1_value), recover

def calculate_systematic_impact_point(df_normalized: pd.DataFrame, baseline: float, t0: pd.Timestamp, t1: pd.Timestamp) -> Tuple[pd.Timestamp, float]:
    """
    Calculates the systematic impact point (tD), which is the minimum point
    in 'in_degree' between t0 and t1.

    Args:
        df_normalized (pd.DataFrame): The DataFrame with normalized 'in_degree' and 'date'.
        baseline (float): The baseline 'in_degree' value.
        t0 (pd.Timestamp): The disaster start date (t0).
        t1 (pd.Timestamp): The recovery/new normal date (t1).

    Returns:
        Tuple[pd.Timestamp, float]: A tuple (tD_date, tD_value).

    Raises:
        Exception: If the range between t0 and t1 is zero, or if no value
                   below the baseline is observed (tD_value >= baseline).
    """
    
    in_recovery_df = df_normalized[(df_normalized["date"] >= t0) & (df_normalized["date"] <= t1)]

    tD_value = in_recovery_df["in_degree"].min()

    if tD_value >= baseline:
        raise Exception("The mobility never went down the baseline during disaster. Abnormal pattern.")

    tD = in_recovery_df[in_recovery_df["in_degree"] == tD_value]["date"].iloc[0]
    tD = pd.to_datetime(tD)

    if tD == t0:
        raise Exception("The mobility went up during disaster. Abnormal pattern")
    
    return tD, tD_value

def calculate_resilience_triangle_metrics(
    df: pd.DataFrame,
    baseline: float,
    disaster_start: pd.Timestamp,
    disaster_end: pd.Timestamp,
) -> dict:
    """
    Calculates all resilience metrics for the Resilience Triangle model for a given CBG.

    Args:
        :param disaster_end: (pd.Timestamp): The end date of the disaster.
        :param disaster_start: (pd.Timestamp): The start date of the disaster.
        :param df: The full dataset.
        :param baseline: has baseline value.

    Returns:
        dict: A dictionary containing calculated points, metrics, and status.
              Returns None if a special case (e.g., error) occurs.
    """

    log_metrics = {
        "resilience": 0.0,
        "robustness": 0.0,
        "vulnerability": 0.0,
        "recovery_status": "New normal",
        "message": None,
        "is_special_case": False,
        "point_t0": None,
        "point_inactive": None,
        "point_tD": None,
        "point_t1": None,
    }

    graph_metrics = {
        "triangle_coordinates": None,
        "disaster_region": (disaster_start, disaster_end),
        "dab_region": None,
        "critical_events": None,
    }

    try:

        point_t0 = calculate_disaster_start_point(df, disaster_start)
        log_metrics["point_t0"] = point_t0[0]

        point_inactive = calculate_disaster_end_point(df, disaster_end)
        log_metrics["point_inactive"] = point_inactive[0]

        point_t1, recovered = calculate_recovery_point(df, disaster_end, baseline)
        log_metrics["point_t1"] = point_t1[0]
        log_metrics["recovery_status"] = "Recovered" if recovered else "New normal"

        point_tD = calculate_systematic_impact_point(df, baseline, point_t0[0], point_t1[0])
        log_metrics["point_tD"] = point_tD[0]

        rpoint_t0 = (point_t0[0], point_t0[1])
        rpoint_tD = (point_tD[0], point_tD[1])
        rpoint_t1 = (point_t1[0], point_t1[1])
        
        relative_t0, relative_tD, relative_t1 = get_relative_points(point_t0, point_tD, point_t1)

        triangle_area = calculate_triangle_area(relative_t0, relative_tD, relative_t1)
        dab_area = get_area_under_baseline(baseline, point_t0[0], point_t1[0])

        if dab_area == 0:
             log_metrics["resilience"] = 0.0
        else:
            log_metrics["resilience"] = (triangle_area / dab_area) * 100

        log_metrics["robustness"] = calculate_slope(rpoint_t1, rpoint_tD)
        log_metrics["vulnerability"] = calculate_slope(rpoint_tD, rpoint_t0)

        graph_metrics["triangle_coordinates"] = rpoint_t0, rpoint_tD, rpoint_t1
        graph_metrics["dab_region"] = rpoint_t0[0], rpoint_t1[0]
        graph_metrics["critical_events"] = {"disaster_start": point_t0[0],
                                            "disaster_end": point_inactive[0],
                                            "systematic_impact": point_tD[0],
                                            "recovery": point_t1[0]
                                            }

    except Exception as e:

        log_metrics["resilience"] = 0.0
        log_metrics["robustness"] = 0.0
        log_metrics["vulnerability"] = 0.0
        log_metrics["is_special_case"] = True
        log_metrics["message"] = str(e)
        log_metrics["recovery_status"] = "No Trend Shown"
        graph_metrics["resilience_triangle"] = False
        graph_metrics["critical_show"] = False
        graph_metrics["fill_dab"] = False

    return log_metrics, graph_metrics