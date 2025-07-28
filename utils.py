# resilience_models/utils.py

import pandas as pd
from datetime import datetime
from typing import Tuple

def calculate_slope(point1: Tuple[datetime, float], point2: Tuple[datetime, float]) -> float:
    """
    Calculates the absolute slope between two points.
    Points should be (date, value) tuples.

    Args:
        point1 (Tuple[datetime, float]): The first point (x1, y1) where x is a datetime object.
        point2 (Tuple[datetime, float]): The second point (x2, y2) where x is a datetime object.

    Returns:
        float: The absolute slope. Returns 1 if x1 equals x2 to avoid division by zero.
    """
    x1, y1 = point1
    x2, y2 = point2
    
    # Convert datetime objects to days for slope calculation
    x1_days = (x1 - datetime(x1.year, 1, 1)).days if isinstance(x1, datetime) else x1
    x2_days = (x2 - datetime(x2.year, 1, 1)).days if isinstance(x2, datetime) else x2

    if x1_days == x2_days:
        return 1  # Handle vertical line as per original notebook
    else:
        slope = (y2 - y1) / (x2_days - x1_days)
        return abs(slope)

def calculate_triangle_area(point1: Tuple[int, float], point2: Tuple[int, float], point3: Tuple[int, float]) -> float:
    """
    Calculates the area of a triangle given three points using the shoelace formula.
    Points should be (date, in_degree) tuples.

    Args:
        point1 (Tuple[datetime, float]): The first point (x1, y1).
        point2 (Tuple[datetime, float]): The second point (x2, y2).
        point3 (Tuple[datetime, float]): The third point (x3, y3).

    Returns:
        float: The area of the triangle.
    """

    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    x3, y3 = point3[0], point3[1]

    area = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    return area

def get_area_under_baseline(baseline_value: float, start_date: pd.Timestamp, end_date: pd.Timestamp) -> float:
    """
    Calculates the area under the baseline from a start date to an end date.

    Args:
        baseline_value (float): The constant baseline value.
        start_date (pd.Timestamp): The start date of the period.
        end_date (pd.Timestamp): The end date of the period.

    Returns:
        float: The calculated area.
    """
    return (end_date - start_date).days * baseline_value

def get_relative_points(point1: Tuple[pd.Timestamp, float], point2: Tuple[pd.Timestamp, float], point3: Tuple[pd.Timestamp, float]) -> Tuple[Tuple[int, float], Tuple[int, float], Tuple[int, float]]:
    """
    Converts absolute datetime points to relative days from the first point.

    Args:
        point1 (Tuple[pd.Timestamp, float]): The reference point (t0).
        point2 (Tuple[pd.Timestamp, float]): The second point (tD).
        point3 (Tuple[pd.Timestamp, float]): The third point (t1).

    Returns:
        Tuple[Tuple[int, float], Tuple[int, float], Tuple[int, float]]:
            A tuple containing three new points (days_relative_to_t0, value).
    """
    point_r1 = (0, point1[1])
    point_r2 = ((point2[0]-point1[0]).days, point2[1])
    point_r3 = ((point3[0]-point1[0]).days, point3[1])
    return (point_r1, point_r2, point_r3)

def log_summary_triangle(
    cbg: str,
    disaster_name: str,
    disaster_start: pd.Timestamp,
    disaster_end: pd.Timestamp,
    point_t0: pd.Timestamp,
    point_inactive: pd.Timestamp,
    point_tD: pd.Timestamp,
    point_t1: pd.Timestamp,
    baseline_value: float,
    resilience: float,
    robustness: float,
    vulnerability: float,
    recovered: bool = False,
    message: str = None,
    is_special_case: bool = False
) -> None:
    """
    Logs a summary of the community resilience analysis (for Triangle model).

    Args:
        cbg (str): The Census Block Group identifier.
        disaster_name (str): The name of the disaster.
        disaster_start (pd.Timestamp): The start date of the disaster.
        disaster_end (pd.Timestamp): The end date of the disaster.
        point_t0 (pd.Timestamp): Disaster start marker.
        point_inactive (pd.Timestamp): Disaster end marker.
        point_tD (pd.Timestamp): Systematic impact marker.
        point_t1 (pd.Timestamp): Recovery detected marker.
        baseline_value (float): The calculated baseline value.
        resilience (float): The calculated resilience percentage.
        robustness (float): The calculated robustness value.
        vulnerability (float): The calculated vulnerability value.
        recovered (bool): True if the CBG recovered, False otherwise.
        message (str): An optional message for special cases.
        is_special_case (bool): True if a special case (e.g., error) occurred.
    """
    print("\n" + "="*70)
    print(f"📍 Community Resilience Summary — {disaster_name} for CBG - {cbg}")
    print("="*70)

    print(f"🗓️  Disaster Timeline:")
    print(f"   • Start: {disaster_start.strftime('%Y-%m-%d')}")
    print(f"   • End  : {disaster_end.strftime('%Y-%m-%d')}")

    print("-" * 70)
    print(f"⏱️  Key Resilience Markers:")
    print(f"   • t0         (Disaster Start)    : {point_t0.strftime('%Y-%m-%d')}")
    print(f"   • t_inactive (Disaster End)    : {point_inactive.strftime('%Y-%m-%d')}")
    print(f"   • tD         (Systematic Impact)    : {point_tD.strftime('%Y-%m-%d')}")
    print(f"   • t1         (Recovery Detected) : {point_t1.strftime('%Y-%m-%d')}")

    print("-" * 70)
    print(f"📉 Baseline Value         : {baseline_value:.4f}")

    print("-" * 70)
    print(f"📊 Resilience Metrics:")
    print(f"   • 🛡️  Robustness     : {robustness:.4f}")
    print(f"   • ⚠️  Vulnerability  : {vulnerability:.4f}")
    print(f"   • 🔁  Resilience      : {resilience:.4f} %")

    print("-" * 70)
    if not is_special_case and recovered:
        print("The CBG was able to recover and comeback to normal")
    elif not is_special_case and not recovered:
        print("The CBG was not able to recover and formed a new normal")

    if is_special_case == True:
        print(f"Special Case - {message}")

    print("="*70 + "\n")

def log_summary_auc(disaster_start: pd.Timestamp, disaster_end: pd.Timestamp, recovery_point: pd.Timestamp, resilience: float) -> None:
    """
    Logs a summary of the community resilience analysis using AUC.

    Args:
        disaster_start (pd.Timestamp): The start date of the disaster.
        disaster_end (pd.Timestamp): The end date of the disaster.
        recovery_point (pd.Timestamp): The date when recovery was achieved.
        resilience (float): The calculated resilience capacity (area under normalized curve).
    """
    print("\nCommunity Resilience Summary")
    print("-----------------------------")
    print(f"Disaster Start Date    : {disaster_start.strftime('%Y-%m-%d')}")
    print(f"Disaster End Date      : {disaster_end.strftime('%Y-%m-%d')}")
    print(f"Recovery Point         : {recovery_point.strftime('%Y-%m-%d')}")
    print(f"Time to Recovery       : {(recovery_point - disaster_start).days} days")
    print(f"Resilience Capacity    : {resilience:.3f} (area under normalized curve)")