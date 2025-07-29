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
        return 0
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