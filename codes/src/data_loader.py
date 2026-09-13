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
    "[/mnt/data/empirical_benchmark_results.csv"](https://gapgpt.app/api/v1/code_interpreter/100563522/84e7c51c-08f5-45fb-99c3-8f2763f10837/.eJwNy0sOgyAQANC7zFoaPiLoWUwmOB0CEa0B7Kbp3du3fx-4G1fMT1iUlHYyVusBKIWO_bXzCQv4kR1ZRUL6aMVo4ybmmYzwUbvJRCW9cTBAzIXxCj39Cx9XrplCwY1PSkeoO1Zud-ntQe29Anx_g5wl-A:1x5cXc:xW8AbI7mBLCYsYU_MQ0Dh0-GO9nYfniy90W1PYTuX5A/empirical_benchmark_results.csv%22)
]

def load_benchmark_data(filepath: Optional[str] = None) -> pd.DataFrame:
    """
    Loads benchmark dataset from CSV or Excel file.
    
    Args:
        filepath: Optional custom path to data file. If None, searches default paths.
        
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
        raise FileNotFoundError(
            "Empirical benchmark data file not found. Ensure 'empirical_benchmark_results.csv' "
            "exists in the root or 'data/' directory."
        )
        
    if target_path.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(target_path)
    else:
        df = pd.read_csv(target_path)
        
    print(f"[INFO] Successfully loaded {len(df)} records from {target_path}")
    return df
