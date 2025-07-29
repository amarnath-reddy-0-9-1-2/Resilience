from visualizations.log_visualization import log_summary_triangle
from visualizations.graph_visualization import plot_resilience_graph_triangle
from data_processing import *
from models.resilience_triangle import calculate_resilience_triangle_metrics


def run_triangle_example():
    """
    Demonstrates the usage of the Resilience Triangle model for a single CBG.
    """
    PATH = "/Users/amarnathreddykalluru/PycharmProjects/Resilience/data/portarthur_sd_df_2019.rdata"
    dataset = "portarthur_sd_df_2019"
    cbg = "483610223005"
    DISASTER_NAME = "Tropical Storm Imelda"
    disaster_start = pd.to_datetime("2019-09-17")
    disaster_end = pd.to_datetime("2019-09-27")

    df = load_and_process_data(PATH, dataset)
    preprocess_df = preprocess_data(df, cbg)
    basline_value = calculate_baseline(preprocess_df, disaster_start)
    log_metrics, graph_metrics = calculate_resilience_triangle_metrics(preprocess_df, basline_value, disaster_start, disaster_end)
    log_summary_triangle(cbg = cbg, baseline_value=basline_value, disaster_name=DISASTER_NAME, **log_metrics)
    plot_resilience_graph_triangle(df = preprocess_df, baseline_value=basline_value, cbg=cbg, **graph_metrics)


if __name__ == "__main__":
    run_triangle_example()