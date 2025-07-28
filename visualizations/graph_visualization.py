# resilience_models/graph_visualization.py

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from typing import List, Tuple, Dict, Optional

def plot_resilience_graph_triangle(
    df: pd.DataFrame,
    triangle_coordinates: Optional[List[Tuple[pd.Timestamp, float]]],
    disaster_region: Tuple[pd.Timestamp, pd.Timestamp],
    dab_region: Optional[Tuple[pd.Timestamp, pd.Timestamp]],
    critical_events: Optional[Dict[str, pd.Timestamp]],
    baseline_value: float,
    plot_baseline: bool = True,
    fill_dab: bool = True,
    disaster_span: bool = True,
    resilience_triangle: bool = True,
    critical_show: bool = True,
    title: str = "Community Resilience (Disaster Impact & Recovery) - Triangle Model",
    cbg: Optional[str] = None
) -> None:
    """
    Plots the resilience graph for the Resilience Triangle model.

    Args:
        df (pd.DataFrame): DataFrame with normalized 'in_degree' and 'date'.
        triangle_coordinates (Optional[List[Tuple[pd.Timestamp, float]]]): List of (date, value) tuples for the triangle vertices (t0, tD, t1).
        disaster_region (Tuple[pd.Timestamp, pd.Timestamp]): Tuple (disaster_start, disaster_end) for the disaster span.
        dab_region (Optional[Tuple[pd.Timestamp, pd.Timestamp]]): Tuple (t0, t1) for the Area Under Baseline fill.
        critical_events (Optional[Dict[str, pd.Timestamp]]): Dictionary of critical event labels and their dates.
        baseline_value (float): The baseline mobility value.
        plot_baseline (bool): Whether to plot the baseline.
        fill_dab (bool): Whether to fill the area under the baseline.
        disaster_span (bool): Whether to show the disaster period span.
        resilience_triangle (bool): Whether to plot and fill the resilience triangle.
        critical_show (bool): Whether to show critical event vertical lines and legend entries.
        title (str): Title of the plot.
        cbg (Optional[str]): CBG identifier to include in the title.
    """
    mask = (df['date'] >= disaster_region[0] - pd.Timedelta(days=30))
    plot_df = df.loc[mask].copy()

    xmax = plot_df['date'].max()
    xmin = plot_df['date'].min()

    fig, ax = plt.subplots(figsize=(15, 8))

    ax.plot(plot_df['date'], plot_df['in_degree'], color='black', linewidth=2, label='Normalized Mobility')

    if plot_baseline:
        ax.hlines(y=baseline_value, xmin=xmin, xmax=xmax, colors='blue', linestyles='--', linewidth=2, label='Baseline')

    if fill_dab and dab_region:
        green_df = df[(df['date'] >= dab_region[0]) & (df['date'] <= dab_region[1])]
        ax.fill_between(
            green_df['date'],
            0,
            baseline_value,
            color='green',
            alpha=0.2,
            label='Area Under Baseline'
        )

    if resilience_triangle and triangle_coordinates and len(triangle_coordinates) == 3:
        x_triangle = [p[0] for p in triangle_coordinates]
        y_triangle = [p[1] for p in triangle_coordinates]
        ax.fill(x_triangle, y_triangle, facecolor='orange', alpha=0.3, label='Resilience Triangle')
        ax.scatter(x_triangle, y_triangle, color='orange', zorder=5)

    if disaster_span:
        ax.axvspan(disaster_region[0], disaster_region[1], color='red', alpha=0.2, label='Disaster Period')

    if critical_show and critical_events:
        plot_handles, plot_labels = ax.get_legend_handles_labels()
        event_styles = {
            'disaster_start': ('darkred', 'left'),
            'disaster_end': ('orangered', 'right'),
            'systematic_impact': ('purple', 'center'),
            'recovery': ('darkgreen', 'right')
        }

        event_handles = []
        for label, date in critical_events.items():
            color, align = event_styles.get(label, ('black', 'center'))
            ax.axvline(x=date, linestyle='--', color=color, linewidth=1.5)
            event_handles.append(Line2D([0], [0], color=color, linestyle="--", label=label.replace('_', ' ').title()))

        all_handles = plot_handles + event_handles
        all_labels = plot_labels + list(critical_events.keys())

        ax.legend(all_handles, all_labels, loc='upper left', fontsize=10, title='Legend')

    full_title = f"{title}"
    if cbg:
        full_title += f" for CBG: {cbg}"
    ax.set_title(full_title, fontsize=16)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Normalized Mobility", fontsize=12)
    ax.set_ylim(0, 1.1)
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_resilience_graph_auc(
    df: pd.DataFrame,
    disaster_region: Tuple[pd.Timestamp, pd.Timestamp],
    resilience_region: Tuple[pd.Timestamp, pd.Timestamp],
    critical_events: Optional[Dict[str, pd.Timestamp]],
    fill_region: bool = True,
    disaster_span: bool = True,
    critical_show: bool = True,
    title: str = "Community Resilience (Disaster Impact & Recovery) - AUC Model",
    cbg: Optional[str] = None
) -> None:
    """
    Plots the resilience graph for the AUC model.

    Args:
        df (pd.DataFrame): DataFrame with baseline-normalized 'in_degree' and 'date'.
        disaster_region (Tuple[pd.Timestamp, pd.Timestamp]): Tuple (disaster_start, disaster_end) for the disaster span.
        resilience_region (Tuple[pd.Timestamp, pd.Timestamp]): Tuple (disaster_start, recovery_point) for the resilience area fill.
        critical_events (Optional[Dict[str, pd.Timestamp]]): Dictionary of critical event labels and their dates.
        fill_region (bool): Whether to fill the resilience area.
        disaster_span (bool): Whether to show the disaster period span.
        critical_show (bool): Whether to show critical event vertical lines and legend entries.
        title (str): Title of the plot.
        cbg (Optional[str]): CBG identifier to include in the title.
    """
    mask = (df['date'] >= disaster_region[0] - pd.Timedelta(days=30))
    plot_df = df.loc[mask].copy()

    max_val = plot_df['in_degree'].abs().max()
    y_limit = max_val if pd.notna(max_val) else 1.0

    fig, ax = plt.subplots(figsize=(15, 8))
    ax.set_ylim(-y_limit * 1.1, y_limit * 1.1)

    ax.plot(plot_df['date'], plot_df['in_degree'], color='black', linewidth=2, label='Normalized Mobility')
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=1.5, alpha=0.8)

    if fill_region:
        fill_mask = (plot_df['date'] >= resilience_region[0]) & (plot_df['date'] <= resilience_region[1])
        fill_df = plot_df.loc[fill_mask].copy() # Ensure copy to avoid SettingWithCopyWarning

        ax.fill_between(
            fill_df['date'],
            fill_df['in_degree'],
            0,  # x-axis baseline
            where=(~fill_df['in_degree'].isna()),
            interpolate=True,
            color='orange',
            alpha=0.3,
            label='Resilience Area'
        )

    if disaster_span:
        ax.axvspan(disaster_region[0], disaster_region[1], color='red', alpha=0.2, label='Disaster Period')

    if critical_show and critical_events:
        plot_handles, plot_labels = ax.get_legend_handles_labels()
        event_styles = {
            'disaster_start': ('darkred', 'left'),
            'disaster_end': ('orangered', 'right'),
            'recovery': ('darkgreen', 'right')
        }

        event_handles = []
        for label, date in critical_events.items():
            color, align = event_styles.get(label, ('black', 'center'))
            ax.axvline(x=date, linestyle='--', color=color, linewidth=1.5)
            event_handles.append(Line2D([0], [0], color=color, linestyle="--", label=label.replace('_', ' ').title()))

        all_handles = plot_handles + event_handles
        all_labels = plot_labels + list(critical_events.keys())

        ax.legend(all_handles, all_labels, loc='upper left', fontsize=10, title='Legend')

    full_title = f"{title}"
    if cbg:
        full_title += f" for CBG: {cbg}"
    ax.set_title(full_title, fontsize=16)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Normalized Mobility", fontsize=12)
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()