# Resilience Models

This is a Python library to help analyze community resilience to disasters. It includes two main models: the **Resilience Triangle Model** and the **Area Under the Curve (AUC) Model**.

## Installation

1.  **Clone this repository**:
    ```bash
    git clone <this_repo_url>
    ```
2.  **Install the necessary libraries**:
    ```bash
    pip install -r requirements.txt
    ```

## Quick Start

1.  **Place your data**: Make sure your `portarthur_sd_df_2019.rdata` file path is set correctly where ever needed.

2.  **Run an example**: I've included some example scripts to show you how it works. You can find them in the `examples/` directory.

    * To see the **Resilience Triangle Model** in action for a specific area:
        ```bash
        python examples/example_triangle_usage.py
        ```
    * To see the **Area Under the Curve (AUC) Model** in action for a specific area:
        ```bash
        python examples/example_auc_usage.py
        ```
    * To process **all areas** and save results to a CSV (using the Triangle model):
        ```bash
        python examples/example_batch_processing.py
        ```

## What it Does

This library helps you:

* **Load and prepare** your mobility data.
* **Calculate resilience metrics** after a disaster, telling you how quickly an area recovers.
* **Visualize** these resilience patterns with graphs.

## Need to Know More?

Check the Python files themselves for more details on specific functions and their parameters.

## License

(No License Yet :)