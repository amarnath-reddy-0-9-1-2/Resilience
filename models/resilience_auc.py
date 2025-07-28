import pandas as pd
import numpy as np

def get_recovery_point_auc(df: pd.DataFrame, disaster_end: pd.Timestamp, threshold: float) -> pd.Timestamp:
    """
    Determines the recovery point for the AUC model.
    The recovery point is the first date after disaster_end where 'in_degree'
    is within the specified threshold of zero (post-baseline normalization).
    If no such point exists, it returns the date with the 'in_degree' closest to zero.

    Args:
        df (pd.DataFrame): The DataFrame with baseline-normalized 'in_degree' and 'date'.
        disaster_end (pd.Timestamp): The end date of the disaster.
        threshold (float): The threshold for 'in_degree' to consider as recovered.

    Returns:
        pd.Timestamp: The calculated recovery date.
    """
    post_disaster_df = df[df["date"] > disaster_end].copy()

    if post_disaster_df.empty:
        return disaster_end

    recovered_within_threshold = post_disaster_df[post_disaster_df["in_degree"].abs() <= threshold]
    if not recovered_within_threshold.empty:
        return recovered_within_threshold["date"].iloc[0]

    closest_idx = post_disaster_df["in_degree"].abs().idxmin()
    return df.loc[closest_idx, "date"]

def compute_auc_between_dates(df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp) -> float:
    """
    Computes the Area Under the Curve (AUC) of the 'in_degree' between two dates
    using the trapezoidal rule.

    Args:
        df (pd.DataFrame): The DataFrame with 'date' and 'in_degree' columns.
        start_date (pd.Timestamp): The start date for AUC computation.
        end_date (pd.Timestamp): The end date for AUC computation.

    Returns:
        float: The calculated AUC. Returns 0.0 if the curve is empty or has less than 2 points.
    """
    curve = df[(df["date"] >= start_date) & (df["date"] <= end_date)].copy()

    if curve.empty or len(curve) < 2:
        return 0.0

    curve = curve.sort_values(by='date')

    curve = curve.set_index("date")
    curve['days'] = (curve.index - curve.index.min()).days

    area = np.trapezoid(curve["in_degree"], curve['days'])

    return area

def calculate_resilience_auc_metrics(
    df: pd.DataFrame,
    disaster_start: pd.Timestamp,
    disaster_end: pd.Timestamp,
    threshold: float
) -> dict:
    """
    Calculates resilience metrics for the Area Under the Curve (AUC) model for a given CBG.

    Args:
        df (pd.DataFrame): The full dataset. baseline normalized.
        disaster_start (pd.Timestamp): The start date of the disaster.
        disaster_end (pd.Timestamp): The end date of the disaster.
        threshold (float): Threshold for determining recovery point in AUC model.

    Returns:
        dict: A dictionary containing calculated metrics and relevant data for plotting.
    """

    log_metrics = {
        "resilience": 0.0,
        "recovery_point": None,
        "disaster_start": disaster_start,
        "disaster_end": disaster_end,
        "message": None,
        "is_special_case": False
    }

    graph_metrics = {
        "disaster_region": None,
        "resilience_region": None,
        "critical_events": None
    }

    try:

        recovery_point = get_recovery_point_auc(df, disaster_end, threshold)
        log_metrics["recovery_point"] = recovery_point

        resilience = compute_auc_between_dates(df, disaster_start, recovery_point)
        log_metrics["resilience"] = resilience

        graph_metrics["disaster_region"] = disaster_start, disaster_end
        graph_metrics["resilience_region"] = disaster_start, recovery_point
        graph_metrics["critical_events"] = {
            "disaster_start": disaster_start,
            "disaster_end": disaster_end,
            "recovery": recovery_point
        }

    except Exception as e:
        log_metrics["resilience_capacity"] = 0.0
        log_metrics["recovery_point"] = None # Reset if error
        log_metrics["message"] = str(e)
        log_metrics["is_special_case"] = True

        graph_metrics["fill_region"] = False
        graph_metrics["critical_show"] = False
        
    return log_metrics, graph_metrics