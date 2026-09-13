# ==============================================================================
# File: R/02_visualizations.R
# Author: Pegah Merrikhi, PhD
# Description: Generates publication-ready figures matching journal palette.
# ==============================================================================

suppressPackageStartupMessages({
  library(tidyverse)
  library(patchwork)
  library(scales)
})

# Custom Journal Color Palette
PALETTE <- list(
  cloud_blue = "#1E3A8A", # Deep Royal Blue
  edge_gold  = "#D97706", # Luminous Gold/Amber
  crimson    = "#991B1B", # Crimson Red
  pink       = "#F43F5E", # Rose Pink
  grid_gray  = "#E5E7EB", # Light Gray
  dark_text  = "#1F2937"  # Slate Gray
)

# Custom Theme
theme_q1_publication <- function() {
  theme_minimal(base_size = 12) +
    theme(
      text = element_text(color = PALETTE$dark_text),
      plot.title = element_text(face = "bold", size = 13, hjust = 0),
      plot.subtitle = element_text(color = "#4B5563", size = 10, margin = margin(b = 10)),
      panel.grid.minor = element_blank(),
      panel.grid.major = element_line(color = PALETTE$grid_gray, linewidth = 0.5),
      axis.title = element_text(face = "bold", size = 10),
      legend.position = "top",
      legend.title = element_text(face = "bold", size = 9),
      plot.background = element_rect(fill = "white", color = NA)
    )
}

# 1. Figure 2: TTFT Latency Comparison
plot_figure2 <- function(df) {
  p_ttft <- ggplot(df, aes(x = language, y = ttft_ms, fill = deployment)) +
    geom_col(position = position_dodge(width = 0.75), width = 0.65, alpha = 0.95) +
    scale_fill_manual(
      values = c("Cloud_GPT4o" = PALETTE$cloud_blue, "Edge_Mamba" = PALETTE$edge_gold),
      labels = c("Cloud (GPT-4o)", "Edge (Mamba-1.4B)")
    ) +
    labs(
      title = "Figure 2: Computational Latency Across Deployments",
      subtitle = "Time-to-First-Token (TTFT) across 5 typologically diverse languages (-72.7% reduction)",
      x = "Linguistic Typology / Language",
      y = "TTFT Latency (ms)",
      fill = "Architecture:"
    ) +
    theme_q1_publication()
  
  return(p_ttft)
}

# 2. Figure 3: Scatter Plot (LHI vs PFS)
plot_figure3 <- function(df) {
  p_scatter <- ggplot(df, aes(x = lhi_score, y = pfs_score)) +
    geom_smooth(method = "lm", color = PALETTE$crimson, fill = PALETTE$pink, alpha = 0.2, linewidth = 1.2) +
    geom_point(aes(color = deployment), size = 4, alpha = 0.9) +
    scale_color_manual(
      values = c("Cloud_GPT4o" = PALETTE$cloud_blue, "Edge_Mamba" = PALETTE$edge_gold),
      labels = c("Cloud Baseline", "Edge Intervention")
    ) +
    annotate(
      "text", x = 0.35, y = 4.7, 
      label = "Spearman rho == -1.000~','~p < .001", parse = TRUE,
      color = PALETTE$crimson, fontface = "bold", size = 4.2
    ) +
    labs(
      title = "Figure 3: Linguistic Homogenisation vs. Pragmatic Fidelity",
      subtitle = "Inverse correlation between standardization and cultural fidelity",
      x = "Linguistic Homogenisation Index (LHI)",
      y = "Pragmatic Fidelity Score (PFS)",
      color = "Deployment Mode:"
    ) +
    theme_q1_publication()
  
  return(p_scatter)
}

# Execution & Export (uncomment to run in R environment)
# ggsave("assets/figure_2_r.png", plot = p2, width = 8, height = 5, dpi = 300)
# ggsave("assets/figure_3_r.png", plot = p3, width = 8, height = 5, dpi = 300)
