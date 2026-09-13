"""
Data loader and preprocessor for empirical benchmark results.
"""

import os
from typing import Optional
import pandas as pd

DEFAULT_DATA_PATHS = [
    "data/empirical_benchmark_results.csv",
    "empirical_benchmark_results.csv",
    "../data/empirical_benchmark_results.csv",
    "/mnt/data/empirical_benchmark_results.csv"
]

def load_benchmark_data(filepath: Optional[str] = None) -> pd.DataFrame:
    """
    Loads benchmark dataset from CSV or Excel file.

    Args:
        filepath: Optional path to data file. If None, default paths are searched.

    Returns:
        pd.DataFrame containing experimental metrics across languages and deployments.
    """
    target_path = filepath
    if target_path is None:
        for p in DEFAULT_DATA_PATHS:
            if os.path.exists(p):
                target_path = p
                break

    if target_path is None or not os.path.exists(target_path):
        raise FileNotFoundError("Empirical benchmark data file not found in default paths.")

    if target_path.endswith('.xlsx') or target_path.endswith('.xls'):
        df = pd.read_excel(target_path)
    else:
        df = pd.read_csv(target_path)

    print(f"[INFO] Loaded {len(df)} records from {target_path}")
    return df
