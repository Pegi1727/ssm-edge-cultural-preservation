"""
Statistical analysis module for benchmarking Edge (Mamba-1.4B) vs Cloud (GPT-4o).
Calculates Wilcoxon signed-rank tests, Paired t-tests, Cohen's dz, and Spearman correlation.
"""

from typing import Dict, Any
import numpy as np
import pandas as pd
from scipy import stats

def compute_cohens_dz(x: np.ndarray, y: np.ndarray) -> float:
    """Calculates Cohen's dz effect size for paired samples."""
    diff = x - y
    std_diff = np.std(diff, ddof=1)
    return float(np.mean(diff) / std_diff) if std_diff != 0 else 0.0

def run_ttft_evaluation(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Executes paired latency (Time-to-First-Token) statistical evaluation.
    """
    cloud_data = df[df['deployment'] == 'Cloud_GPT4o'].sort_values('language')
    edge_data = df[df['deployment'] == 'Edge_Mamba'].sort_values('language')
    
    if len(cloud_data) != len(edge_data) or len(cloud_data) == 0:
        raise ValueError("Mismatched or missing paired records between Cloud and Edge.")
        
    cloud_ttft = cloud_data['ttft_ms'].to_numpy()
    edge_ttft = edge_data['ttft_ms'].to_numpy()
    
    # Wilcoxon signed-rank test
    w_stat, w_pval = stats.wilcoxon(cloud_ttft, edge_ttft)
    
    # Paired Student's t-test
    t_stat, t_pval = stats.ttest_rel(cloud_ttft, edge_ttft)
    
    # Cohen's dz effect size
    dz = compute_cohens_dz(cloud_ttft, edge_ttft)
    
    mean_reduction_pct = float(np.mean((cloud_ttft - edge_ttft) / cloud_ttft) * 100)
    
    return {
        "cloud_mean_ttft_ms": float(np.mean(cloud_ttft)),
        "cloud_sd_ttft_ms": float(np.std(cloud_ttft, ddof=1)),
        "edge_mean_ttft_ms": float(np.mean(edge_ttft)),
        "edge_sd_ttft_ms": float(np.std(edge_ttft, ddof=1)),
        "latency_reduction_pct": mean_reduction_pct,
        "wilcoxon_stat": float(w_stat),
        "wilcoxon_p_value": float(w_pval),
        "t_stat": float(t_stat),
        "t_p_value": float(t_pval),
        "cohens_dz": dz
    }

def run_correlation_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes Spearman rank correlation between Linguistic Homogenisation Index (LHI)
    and Pragmatic Fidelity Score (PFS).
    """
    if 'lhi_score' not in df.columns or 'pfs_score' not in df.columns:
        raise KeyError("Columns 'lhi_score' and 'pfs_score' are required for correlation analysis.")
        
    rho, pval = stats.spearmanr(df['lhi_score'], df['pfs_score'])
    
    return {
        "spearman_rho": float(rho),
        "p_value": float(pval)
    }

def generate_full_report(df: pd.DataFrame) -> Dict[str, Any]:
    """Runs all evaluations and aggregates results."""
    ttft_results = run_ttft_evaluation(df)
    corr_results = run_correlation_analysis(df)
    return {
        "latency_analysis": ttft_results,
        "homogenisation_vs_fidelity": corr_results
    }
