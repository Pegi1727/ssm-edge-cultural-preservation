#!/usr/bin/env python3
"""Paired Cloud-versus-Edge benchmark analysis for five languages."""
import argparse
from itertools import product
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

METRICS = ["TTFT_ms", "TFF", "LHI", "PFS"]
LANGUAGES = ["Persian", "Azerbaijani", "Turkish", "Russian", "English"]
CONDITIONS = ["Cloud", "Edge"]


def load_raw(path):
    """Load raw observations from the workbook's Benchmark Data sheet or raw CSV."""
    path = Path(path)
    if path.suffix.lower() in (".xlsx", ".xlsm", ".xls"):
        df = pd.read_excel(path, sheet_name="Benchmark Data")
    elif path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        raise ValueError("Input must be .xlsx, .xlsm, .xls, or a raw .csv")
    required = {"Language", "Condition", *METRICS}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing raw columns: {sorted(missing)}; summary-only input is not supported")
    df = df[["Language", "Condition", *METRICS]].copy()
    for col in ["Language", "Condition"]:
        df[col] = df[col].astype("string").str.strip()
    df["Condition"] = df["Condition"].str.casefold().map({"cloud":"Cloud", "edge":"Edge"})
    if df[["Language", "Condition"]].isna().any().any():
        raise ValueError("Language and Condition cannot be blank or unrecognized")
    actual_langs = set(df.Language.astype(str))
    if actual_langs != set(LANGUAGES):
        raise ValueError(f"Expected exactly {LANGUAGES}; found {sorted(actual_langs)}")
    if set(df.Condition.astype(str)) != set(CONDITIONS):
        raise ValueError("Condition values must be Cloud and Edge")
    if df[["Language", "Condition"]].duplicated().any():
        raise ValueError("Duplicate Language/Condition observations")
    expected = {(language, condition) for language in LANGUAGES for condition in CONDITIONS}
    actual = set(zip(df.Language.astype(str), df.Condition.astype(str)))
    if actual != expected:
        raise ValueError(f"Expected exactly one complete Cloud/Edge pair per language; missing={sorted(expected-actual)}")
    for metric in METRICS:
        df[metric] = pd.to_numeric(df[metric], errors="raise")
        if not np.isfinite(df[metric].to_numpy(dtype=float)).all():
            raise ValueError(f"{metric} contains missing or non-finite values")
    return df.sort_values(["Language", "Condition"], key=lambda s: s.map({x:i for i,x in enumerate(LANGUAGES)}) if s.name == "Language" else s).reset_index(drop=True)


def exact_wilcoxon(differences):
    """Exact two-sided sign-enumeration Wilcoxon; zero differences are discarded."""
    x = np.asarray(differences, dtype=float)
    x = x[x != 0]
    if len(x) == 0:
        return 0.0, 1.0
    ranks = stats.rankdata(np.abs(x), method="average")
    observed = min(float(ranks[x > 0].sum()), float(ranks[x < 0].sum()))
    rank_sum = float(ranks.sum())
    # Enumerating sign assignments handles tied absolute differences exactly.
    tail = 0
    for signs in product((-1, 1), repeat=len(x)):
        positive = sum(rank for rank, sign in zip(ranks, signs) if sign > 0)
        if min(float(positive), rank_sum-float(positive)) <= observed + 1e-12:
            tail += 1
    return observed, tail / (2 ** len(x))


def analyze(df, outdir):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    summary, per_language = [], []
    for metric in METRICS:
        paired = df.pivot(index="Language", columns="Condition", values=metric).reindex(LANGUAGES)
        cloud = paired["Cloud"].to_numpy(dtype=float)
        edge = paired["Edge"].to_numpy(dtype=float)
        diff = cloud - edge  # Sign convention throughout: Cloud minus Edge.
        n = len(diff)
        t_result = stats.ttest_1samp(diff, popmean=0.0)
        if n > 1 and np.std(diff, ddof=1) > 0:
            ci_low, ci_high = stats.t.interval(0.95, n-1, loc=np.mean(diff), scale=stats.sem(diff))
            dz = float(np.mean(diff) / np.std(diff, ddof=1))
        else:
            ci_low = ci_high = dz = np.nan
        w, p_w = exact_wilcoxon(diff)
        p_t_adj = min(float(t_result.pvalue) * len(METRICS), 1.0)
        p_w_adj = min(float(p_w) * len(METRICS), 1.0)
        cm, em = float(np.mean(cloud)), float(np.mean(edge))
        summary.append({
            "metric": metric, "n_languages": n, "cloud_mean": cm,
            "cloud_sd": float(np.std(cloud, ddof=1)), "edge_mean": em,
            "edge_sd": float(np.std(edge, ddof=1)),
            "mean_diff_cloud_minus_edge": float(np.mean(diff)),
            "sd_paired_difference": float(np.std(diff, ddof=1)),
            "paired_t": float(t_result.statistic), "t_df": n-1,
            "p_t_two_sided": float(t_result.pvalue), "ci95_low": float(ci_low),
            "ci95_high": float(ci_high), "cohens_dz": dz,
            "wilcoxon_W": w, "p_wilcoxon_exact_two_sided": p_w,
            "p_t_bonferroni_4": p_t_adj, "p_wilcoxon_bonferroni_4": p_w_adj,
            "edge_change_percent_vs_cloud": (em-cm)/cm*100 if cm else np.nan,
            "paired_t_significant_bonferroni_0.05": bool(p_t_adj < 0.05),
            "wilcoxon_significant_bonferroni_0.05": bool(p_w_adj < 0.05),
        })
        for lang, c, e, d in zip(LANGUAGES, cloud, edge, diff):
            per_language.append({"Language":lang,"metric":metric,"cloud":c,"edge":e,
                                "difference_cloud_minus_edge":d,
                                "edge_change_percent_vs_cloud":(e-c)/c*100 if c else np.nan})
    summary_df = pd.DataFrame(summary)
    per_df = pd.DataFrame(per_language)
    summary_df.to_csv(outdir/"results_summary.csv", index=False, float_format="%.10g")
    per_df.to_csv(outdir/"per_language_results.csv", index=False, float_format="%.10g")

    # Exploratory LHI-PFS correlations within each condition and across paired changes.
    corr_rows = []
    for condition in CONDITIONS:
        sub = df.loc[df.Condition == condition].set_index("Language").reindex(LANGUAGES)
        result = stats.spearmanr(sub["LHI"].to_numpy(float), sub["PFS"].to_numpy(float))
        corr_rows.append({"analysis":"Within-condition LHI vs PFS", "condition":condition,
                          "n":len(sub), "spearman_rho":float(result.statistic),
                          "p_two_sided":float(result.pvalue),
                          "note":"Exploratory only; n=5 language-level observations; report separately by condition."})
    wide = {metric: df.pivot(index="Language", columns="Condition", values=metric).reindex(LANGUAGES) for metric in METRICS}
    d_lhi = (wide["LHI"]["Cloud"] - wide["LHI"]["Edge"]).to_numpy(float)
    d_pfs = (wide["PFS"]["Cloud"] - wide["PFS"]["Edge"]).to_numpy(float)
    result = stats.spearmanr(d_lhi, d_pfs)
    corr_rows.append({"analysis":"Correlation between paired changes", "condition":"Cloud minus Edge changes",
                      "n":len(LANGUAGES), "spearman_rho":float(result.statistic),
                      "p_two_sided":float(result.pvalue),
                      "note":"Exploratory correlation of paired LHI and PFS changes; n=5 languages."})
    corr_df = pd.DataFrame(corr_rows)
    corr_df.to_csv(outdir/"correlation_exploratory.csv", index=False, float_format="%.10g")
    return summary_df, per_df, corr_df


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", help="Raw workbook (.xlsx) or CSV; defaults to adjacent empirical_benchmark_results.xlsx")
    parser.add_argument("--outdir", default=".", help="Directory for result CSV files")
    args = parser.parse_args()
    source = Path(args.source) if args.source else Path(__file__).with_name("empirical_benchmark_results.xlsx")
    summary, _, _ = analyze(load_raw(source), args.outdir)
    print(summary.to_string(index=False))
    print(f"\nWrote results_summary.csv, per_language_results.csv, correlation_exploratory.csv to {Path(args.outdir).resolve()}")

if __name__ == "__main__":
    main()
