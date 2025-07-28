# Community Resilience Analysis Library

A Python library for analyzing community resilience to disasters using the **Resilience Triangle Model** and **Area Under the Curve (AUC) Model**. This toolset provides robust methods to quantify and visualize recovery patterns from mobility data.

## Features

- **Data Preparation**: Load and preprocess mobility data for resilience analysis.
- **Resilience Metrics**: Calculate recovery metrics post-disaster, including speed and extent of recovery.
- **Visualization**: Generate insightful graphs to illustrate resilience patterns.
- **Batch Processing**: Analyze multiple areas and export results to CSV for comprehensive studies.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/amarnath-reddy-0-9-1-2/Resilience.git
   cd Resilience
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.8+ installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

1. **Prepare Your Data**:
   - Place your `portarthur_sd_df_2019.rdata` file in the appropriate directory.
   - Update the file path in the scripts or configuration as needed.

2. **Run Example Scripts**:
   Example scripts are located in the `examples/` directory. Use them to explore the library’s capabilities:

   - **Resilience Triangle Model**:
     ```bash
     python examples/run_triangle_example.py
     ```
     Demonstrates the Resilience Triangle Model for a single area.

   - **Area Under the Curve (AUC) Model**:
     ```bash
     python examples/run_auc_example.py
     ```
     Shows the AUC Model for a single area.

   - **Batch Processing**:
     ```bash
     python examples/batch_processing.py
     ```
     Processes all areas using the Triangle Model and saves results to a CSV file.

## Author
- **Amarnath Reddy Kalluru**
- Email: [amarnathreddykalluru@gmail.com](mailto:amarnathreddykalluru@gmail.com)