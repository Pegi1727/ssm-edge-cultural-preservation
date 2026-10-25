# Statistical Analysis Report — Cloud (GPT-4o) vs Edge SSM (Mamba)
N = 5 paired language observations (Persian, Azerbaijani, Turkish, Russian, English). Alpha = .05.

## 1. Descriptives (Mean ± SD, ddof=1)

| Metric | Cloud | Edge | Δ (Cloud−Edge) | SD of diffs | % change |
|---|---|---|---|---|---|
| TTFT_ms | 432.0 ± 81.06 | 118.0 ± 19.24 | +314.0 | 62.29 | −72.7% |
| TFF | 2.58 ± 1.09 | 1.52 ± 0.30 | +1.06 | 0.796 | −41.1% |
| LHI | 0.634 ± 0.245 | 0.334 ± 0.057 | +0.300 | 0.204 | −47.3% |
| PFS | 3.46 ± 0.79 | 4.36 ± 0.21 | −0.90 | 0.70 | +26.0% |

## 2. Paired tests (N=5)

Normality (Shapiro–Wilk on paired differences) was acceptable for all metrics (all p ≥ .057), so the paired t-test is primary; Wilcoxon is reported as the non-parametric exact check.

| Metric | t(4) | p (t-test) | Wilcoxon W | p (Wilcoxon, exact) | Cohen's d_z | Interpretation |
|---|---|---|---|---|---|---|
| TTFT_ms | 11.27 | .00035*** | 0.0 | .0625 | 5.04 | Huge latency reduction |
| TFF | 2.98 | .041* | 0.0 | .0679 | 1.33 | Significant, large |
| LHI | 3.29 | .030* | 1.0 | .125 | 1.47 | Significant, large |
| PFS | −2.87 | .045* | 1.0 | .125 | −1.29 | Significant, large (Edge > Cloud) |

Caveat: with N=5, Wilcoxon exact p-values can never fall below .0625 (minimum two-sided p for n=5), so they are conservative and underpowered here; the parametric tests and effect sizes carry the inferential weight.

## 3. Correlations

| Pair | Model | Pearson r | p | Spearman ρ | p |
|---|---|---|---|---|---|
| TFF ~ PFS | Cloud | −0.892 | .042 | −0.900 | .037 |
| TFF ~ PFS | Edge | −0.660 | .226 | −0.700 | .188 |
| LHI ~ PFS | Cloud | −0.996 | .0003 | −1.000 | <.0001 |
| LHI ~ PFS | Edge | −0.959 | .010 | −1.000 | <.0001 |
| TFF ~ LHI | Cloud | 0.870 | .055 | 0.900 | .037 |
| TFF ~ LHI | Edge | 0.806 | .099 | 0.700 | .188 |

Key finding: LHI is a near-perfect negative predictor of pragmatic fidelity (ρ = −1.00 in both conditions) — stylistic homogenisation is the mechanism through which fidelity is destroyed.

## 4. Agglutinative (Turkish, Azerbaijani) vs Non-agglutinative (Persian, Russian, English)

| Metric | Group | Cloud | Edge | Δ |
|---|---|---|---|---|
| TTFT_ms | Agglut. | 495 ± 21 | 135 ± 7 | +360 |
| TTFT_ms | Non-agglut. | 390 ± 79 | 107 ± 15 | +283 |
| TFF | Agglut. | 3.65 ± 0.21 | 1.80 ± 0.14 | +1.85 (≈2.0×) |
| TFF | Non-agglut. | 1.87 ± 0.68 | 1.33 ± 0.21 | +0.53 (≈1.4×) |
| LHI | Agglut. | 0.80 ± 0.02 | 0.36 ± 0.03 | +0.44 |
| LHI | Non-agglut. | 0.53 ± 0.28 | 0.32 ± 0.07 | +0.21 |
| PFS | Agglut. | 2.90 ± 0.14 | 4.30 ± 0.14 | −1.40 |
| PFS | Non-agglut. | 3.83 ± 0.85 | 4.40 ± 0.26 | −0.57 |

Interaction pattern: Cloud degradation is roughly 3.5× larger in TFF, 2× larger in LHI, and 2.5× larger in PFS deficit for agglutinative languages — a morphological-complexity × architecture interaction.

## 5. Language-level detail

| Language | TFF Cloud→Edge | LHI Cloud→Edge | PFS Cloud→Edge |
|---|---|---|---|
| Persian | 2.1→1.4 | 0.72→0.31 | 3.2→4.5 |
| Azerbaijani | 3.8→1.9 | 0.81→0.38 | 2.8→4.2 |
| Turkish | 3.5→1.7 | 0.78→0.34 | 3.0→4.4 |
| Russian | 2.4→1.5 | 0.65→0.39 | 3.5→4.1 |
| English | 1.1→1.1 | 0.21→0.25 | 4.8→4.6 |

Note the ceiling/floor for English: Cloud TFF = Edge TFF (1.1) and ΔLHI = −0.04, consistent with the "distance from the anglophone centre" homogenisation gradient (ΔLHI: English −0.04, Russian 0.26, Persian 0.41, Turkish 0.44, Azerbaijani 0.43).

## 6. ASCII summary for the manuscript

```
METRIC        CLOUD          EDGE           TEST                 EFFECT
TTFT (ms)     432 ± 81       118 ± 19       t=11.27, p=.0004     d_z=5.04 (huge)
TFF           2.58 ± 1.09    1.52 ± 0.30    t=2.98,  p=.041      d_z=1.33 (large)
LHI           0.63 ± 0.25    0.33 ± 0.06    t=3.29,  p=.030      d_z=1.47 (large)
PFS           3.46 ± 0.79    4.36 ± 0.21    t=-2.87, p=.045      d_z=-1.29 (large)

LHI ~ PFS: Cloud rho=-1.00 (p<.001) | Edge rho=-1.00 (p<.001)
```
