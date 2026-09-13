# install_dependencies.R
# Script to install all required R packages for the project

required_packages <- c(
  "tidyverse",    # Data manipulation & ggplot2
  "rstatix",      # Statistical tests (Wilcoxon, t-test)
  "effsize",      # Effect sizes (Cohen's d)
  "patchwork",    # Combining ggplots
  "scales",       # Plot formatting
  "knitr",        # Dynamic reports
  "rmarkdown",    # Rmd rendering
  "readxl"        # Excel file import
)

new_packages <- required_packages[!(required_packages %in% installed.packages()[, "Package"])]

if (length(new_packages) > 0) {
  install.packages(new_packages, repos = "https://cloud.r-project.org/")
  message("All required packages installed successfully.")
} else {
  message("All packages are already installed.")
}
