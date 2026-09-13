"""
Main Execution Script for Reproducing Empirical Benchmarks and Figures.
Author: Pegah Merrikhi, PhD
"""

import sys
import os
import json

from src.data_loader import load_benchmark_data
from src.statistical_analysis import generate_full_report
from src.visualizations import plot_figure_2_latency, plot_figure_3_correlation

def main():
    print("==================================================================")
    print("  Decentralizing Linguistic Sovereignty: Empirical Evaluation     ")
    print("  Author: Pegah Merrikhi, PhD                                    ")
    print("==================================================================")
    
    # 1. Load Data
    try:
        df = load_benchmark_data()
    except Exception as e:
        print(f"[ERROR] Failed to load dataset: {e}")
        sys.exit(1)
        
    # 2. Run Statistical Report
    print("\n[1/3] Executing Statistical Benchmarking...")
    report = generate_full_report(df)
    print(json.dumps(report, indent=4))
    
    # 3. Generate Visual Assets
    print("\n[2/3] Generating High-Resolution Figures...")
    os.makedirs("assets", exist_ok=True)
    plot_figure_2_latency(df, output_path="assets/figure_2_latency.png")
    plot_figure_3_correlation(df, output_path="assets/figure_3_correlation.png")
    
    print("\n[3/3] Execution completed successfully. All artifacts created in assets/")
    print("==================================================================")

if __name__ == "__main__":
    main()
