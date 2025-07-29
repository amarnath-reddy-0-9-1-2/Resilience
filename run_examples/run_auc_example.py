import pandas as pd
from data_processing import *
from models.resilience_auc import *
from visualizations.graph_visualization import plot_resilience_graph_auc
from visualizations.log_visualization import log_summary_auc


def run_auc_example():
    """
    Demonstrates the usage of the Resilience Triangle model for a single CBG.
    """
    PATH = "/Users/amarnathreddykalluru/PycharmProjects/Resilience/data/portarthur_sd_df_2019.rdata"
    dataset = "portarthur_sd_df_2019"
    cbg = "483610223005"
    DISASTER_NAME = "Tropical Storm Imelda"
    disaster_start = pd.to_datetime("2019-09-17")
    disaster_end = pd.to_datetime("2019-09-27")
    threshold = 0.01

    df = load_and_process_data(PATH, dataset)
    preprocess_df = preprocess_data(df, cbg)
    basline_value = calculate_baseline(preprocess_df, disaster_start)
    bn_df = baseline_normalization(preprocess_df, basline_value)
    log_metrics, graph_metrics = calculate_resilience_auc_metrics(bn_df, disaster_start, disaster_end, threshold)
    log_summary_auc(cbg=cbg, disaster_name=DISASTER_NAME, **log_metrics)
    plot_resilience_graph_auc(df=bn_df, cbg=cbg, **graph_metrics)

if __name__ == "__main__":
    run_auc_example()