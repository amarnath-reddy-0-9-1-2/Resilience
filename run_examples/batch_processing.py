from data_processing import *
from models.resilience_triangle import *

def run_batch_processing():

    PATH = "/Users/amarnathreddykalluru/PycharmProjects/Resilience/data/portarthur_sd_df_2019.rdata"
    dataset = "portarthur_sd_df_2019"
    disaster_start = pd.to_datetime("2019-09-17")
    disaster_end = pd.to_datetime("2019-09-27")

    df = load_and_process_data(PATH, dataset)

    all_cbgs = list(df['destination_cbg'].unique())
    print("Total no. of cbgs - ", len(all_cbgs))

    all_cbg_resilience = {"CBG": [], "Resilience": [], "Robustuness": [], "Vulnerability": [], "Status": []}

    special_count = 0

    for cbg in all_cbgs:
        print("Processing cbg", cbg)
        preprocess_df = preprocess_data(df, cbg)
        basline_value = calculate_baseline(preprocess_df, disaster_start)
        log_metrics, _ = calculate_resilience_triangle_metrics(preprocess_df, basline_value, disaster_start, disaster_end)
        if log_metrics["is_special_case"]:
            print("special_case detected - ", cbg)
            special_count += 1
        all_cbg_resilience["CBG"].append(cbg)
        all_cbg_resilience["Resilience"].append(log_metrics["resilience"])
        all_cbg_resilience["Robustuness"].append(log_metrics["robustness"])
        all_cbg_resilience["Vulnerability"].append(log_metrics["vulnerability"])
        all_cbg_resilience["Status"].append(log_metrics["recovery_status"])

    print("Total no. of cbgs - ", len(all_cbgs))
    print("Total no. of special cbgs - ", special_count)
    print("Total no. of normal cbgs - ", len(all_cbgs)-special_count)

    resilience_df = pd.DataFrame(all_cbg_resilience)
    resilience_df.to_csv("cbg_resilience_summary.csv", index=False)

    data = pd.read_csv('../cbg_resilience_summary.csv')
    new_data = data[data["Status"] != "No Trend Shown"]
    new_data.to_csv('cbg_resilience_summary_filtered.csv', index=False)

if __name__ == "__main__":
    run_batch_processing()