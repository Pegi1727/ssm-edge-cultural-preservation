# ==============================================================================
# File: R/01_statistical_benchmarking.R
# Author: Pegah Merrikhi, PhD
# Description: Rigorous statistical evaluation of Edge (Mamba-1.4B) vs Cloud 
#              (GPT-4o) baseline across typologically diverse languages.
# ==============================================================================

suppressPackageStartupMessages({
  library(tidyverse)
  library(rstatix)
  library(effsize)
})

# 1. Load Data
data_path <- file.path("data", "empirical_benchmark_results.csv")
if (!file.exists(data_path)) {
  data_path <- "empirical_benchmark_results.csv" # fallback
}

if (!file.exists(data_path)) {
  stop("Dataset file 'empirical_benchmark_results.csv' not found.")
}

benchmark_df <- read_csv(data_path, show_col_types = FALSE)
message("Dataset loaded successfully: ", nrow(benchmark_df), " observations.")

# 2. Descriptive Summary
summary_stats <- benchmark_df %>%
  group_by(deployment) %>%
  summarise(
    mean_ttft = mean(ttft_ms, na.rm = TRUE),
    sd_ttft   = sd(ttft_ms, na.rm = TRUE),
    mean_tff  = mean(tff_ratio, na.rm = TRUE),
    mean_lhi  = mean(lhi_score, na.rm = TRUE),
    mean_pfs  = mean(pfs_score, na.rm = TRUE),
    .groups   = "drop"
  )

print("--- Descriptive Statistics Summary ---")
print(summary_stats)

# 3. Paired Statistical Testing (TTFT Cloud vs Edge)
# Checking normality of differences
ttft_cloud <- benchmark_df %>% filter(deployment == "Cloud_GPT4o") %>% pull(ttft_ms)
ttft_edge  <- benchmark_df %>% filter(deployment == "Edge_Mamba") %>% pull(ttft_ms)

if (length(ttft_cloud) == length(ttft_edge) && length(ttft_cloud) > 0) {
  diffs <- ttft_cloud - ttft_edge
  
  # Wilcoxon Signed-Rank Test (Paired)
  wilcox_res <- wilcox.test(ttft_cloud, ttft_edge, paired = TRUE, exact = FALSE)
  
  # Paired t-test
  t_res <- t.test(ttft_cloud, ttft_edge, paired = TRUE)
  
  # Cohen's dz Effect Size
  cohen_res <- cohen.d(ttft_cloud, ttft_edge, paired = TRUE)
  
  cat("\n===========================================\n")
  cat("--- TTFT Inference Results ---\n")
  cat(sprintf("Wilcoxon V: %.2f, p-value: %.5e\n", wilcox_res$statistic, wilcox_res$p.value))
  cat(sprintf("Paired t-test t: %.4f, p-value: %.5e\n", t_res$statistic, t_res$p.value))
  cat(sprintf("Cohen's dz: %.4f (Magnitude: %s)\n", cohen_res$estimate, cohen_res$magnitude))
  cat("===========================================\n")
}

# 4. Correlation: Linguistic Homogenisation (LHI) vs Pragmatic Fidelity (PFS)
if ("lhi_score" %in% colnames(benchmark_df) && "pfs_score" %in% colnames(benchmark_df)) {
  spearman_res <- cor.test(benchmark_df$lhi_score, benchmark_df$pfs_score, method = "spearman", exact = FALSE)
  
  cat("\n--- Spearman Rank Correlation (LHI vs PFS) ---\n")
  cat(sprintf("Spearman's rho: %.4f, p-value: %.5e\n", spearman_res$estimate, spearman_res$p.value))
}
