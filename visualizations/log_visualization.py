from typing import Optional

import pandas as pd


def log_summary_triangle(
    cbg: str,
    point_t0: pd.Timestamp,
    point_inactive: pd.Timestamp,
    point_tD: pd.Timestamp,
    point_t1: pd.Timestamp,
    baseline_value: float,
    resilience: float,
    robustness: float,
    vulnerability: float,
    disaster_name: Optional[str] = None,
    recovery_status: str = "Recovered",
    message: str = None,
    is_special_case: bool = False
) -> None:
    """
    Logs a summary of the community resilience analysis (for Triangle model).

    Args:
        :param cbg: The Census Block Group identifier.
        :param disaster_name: The name of the disaster.
        :param disaster_start: The start date of the disaster.
        :param disaster_end: The end date of the disaster.
        :param point_t0: Disaster start marker.
        :param point_inactive: Disaster end marker.
        :param point_tD: Systematic impact marker.
        :param point_t1: Recovery detected marker.
        :param baseline_value: The calculated baseline value.
        :param resilience: The calculated resilience percentage.
        :param robustness: The calculated robustness value.
        :param vulnerability: The calculated vulnerability value.
        :param recovery_status: True if the CBG recovered, False otherwise.
        :param message: An optional message for special cases.
        :param is_special_case: True if a special case (e.g., error) occurred.
    """
    print("\n" + "="*70)
    print(f"📍 Community Resilience Summary for CBG - {cbg} - {disaster_name}")

    print("="*70)

    print(f"🗓️  Disaster Timeline:")
    print(f"   • Start: {point_t0.strftime('%Y-%m-%d')}")
    print(f"   • End  : {point_inactive.strftime('%Y-%m-%d')}")

    print("-" * 70)
    print(f"⏱️  Key Resilience Markers:")
    print(f"   • t0         (Disaster Start)    : {point_t0}")
    print(f"   • t_inactive (Disaster End)    : {point_inactive}")
    print(f"   • tD         (Systematic Impact)    : {point_tD}")
    print(f"   • t1         (Recovery Detected) : {point_t1}")

    print("-" * 70)
    print(f"📉 Baseline Value         : {baseline_value:.4f}")

    print("-" * 70)
    print(f"📊 Resilience Metrics:")
    print(f"   • 🛡️  Robustness     : {robustness:.4f}")
    print(f"   • ⚠️  Vulnerability  : {vulnerability:.4f}")
    print(f"   • 🔁  Resilience      : {resilience:.4f} %")

    print("-" * 70)
    print(f"Recovery Status: {recovery_status}")

    if is_special_case:
        print(f"Special Case - {message}")

    print("="*70 + "\n")

def log_summary_auc(
        cbg: str,
        disaster_start: pd.Timestamp,
        disaster_end: pd.Timestamp,
        recovery_point: pd.Timestamp,
        resilience: float,
        is_special_case: True,
        disaster_name: Optional[str] = None,
        message: str = None
        ) -> None:
    """
    Logs a summary of the community resilience analysis using AUC.

    Args:
        cbg: The Census Block Group identifier.

        disaster_start (pd.Timestamp): The start date of the disaster.
        disaster_end (pd.Timestamp): The end date of the disaster.
        recovery_point (pd.Timestamp): The date when recovery was achieved.
        resilience (float): The calculated resilience capacity (area under normalized curve).
        is_special_case (bool): True if a special case (e.g., error) occurred.
        disaster_name: The name of the disaster.
        message (str): An optional message for special cases.
    """
    print(f"\nCommunity Resilience Summary for {cbg} - {disaster_name}")
    print("-----------------------------")
    print(f"Disaster Start Date    : {disaster_start.strftime('%Y-%m-%d')}")
    print(f"Disaster End Date      : {disaster_end.strftime('%Y-%m-%d')}")
    print(f"Recovery Point         : {recovery_point.strftime('%Y-%m-%d')}")
    print(f"Time to Recovery       : {(recovery_point - disaster_start).days} days")
    print(f"Resilience Capacity    : {resilience:.3f} (area under normalized curve)")

    if is_special_case:
        print(f"Special Case - {message}")