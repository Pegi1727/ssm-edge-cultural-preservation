# Empirical benchmark analysis: Cloud vs Edge

Reproducible paired analysis for the five languages in the Excel workbook's `Benchmark Data` sheet. Source columns required: `Language`, `Condition`, `TTFT_ms`, `TFF`, `LHI`, `PFS`. The loader validates exactly one Cloud and Edge observation for each of Persian, Azerbaijani, Turkish, Russian, and English; it rejects incomplete, duplicate, non-numeric, or summary-only input.

## Methods and interpretation

Each paired difference is **Cloud − Edge**. The summary reports condition means/sample SDs, paired mean and SD difference, paired two-sided t test and 95% t confidence interval, Cohen's *dz* (mean paired difference / SD paired difference), exact two-sided Wilcoxon signed-rank test (zeros discarded; ties in absolute differences handled by average ranks), and Bonferroni-adjusted p-values. The correction is applied separately to the four paired t tests and four Wilcoxon tests (multiply each p by 4, capped at 1).

Spearman correlations are exploratory: LHI versus PFS is reported separately in Cloud and Edge, plus a correlation of the paired changes. These are based on only five language-level observations; p-values and rank associations are unstable and should not be treated as confirmatory or causal. The unit of analysis is language, not repeated runs or independent speakers.

## Run

```bash
python -m pip install -r requirements.txt
python analysis.py /path/to/empirical_benchmark_results.xlsx --outdir .
# Raw CSV is also accepted:
python analysis.py /path/to/raw.csv --outdir results
```

The workbook is the source for observations. The script writes `results_summary.csv`, `per_language_results.csv`, and `correlation_exploratory.csv`. The workbook is deliberately not duplicated in this GitHub artifact bundle; supply it as the input path when running.

## Current data check

For the attached data, the five language pairs reproduce Cloud means of 432.0 ms (TTFT), 2.58 (TFF), 0.634 (LHI), and 3.46 (PFS), versus Edge means 118.2 ms, 1.52, 0.334, and 4.36. With five pairs, the exact two-sided Wilcoxon test has a minimum attainable p-value of 0.0625 when there are no zero differences; a non-significant Wilcoxon result does not establish equivalence. Interpret the paired t results cautiously given the tiny sample.

## Contents

- `analysis.py` — validated loader, statistical analysis, and CLI.
- `results_summary.csv` — metric-level inferential results and effect sizes.
- `per_language_results.csv` — paired values and changes by language.
- `correlation_exploratory.csv` — separate exploratory Spearman analyses.
- `requirements.txt` — Python dependencies.
