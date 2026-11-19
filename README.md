# Blind Cognitive Multi-Factor Authentication (BC-MFA) under OpenID Connect

Research paper, LaTeX source, and reproducibility artifact developed for the course **Web and Mobile Systems Security** (*M.Sc. in Cybersecurity and Computer Systems Auditing*, Polytechnic Institute of Gaya — ISPGAYA, 2026/2027).

**Author:** Carlos André Sousa (`casousa@ispgaya.pt`)

## Overview

BC-MFA is a hardware-free step-up authentication architecture designed for untrusted web and mobile public clients exposed to unprivileged user-space infostealers, screen scrapers, keyloggers, and carrier-level SIM swapping. It combines:

- **$4 \times 4$ quadrant-balanced toroidal permutation matrices** ($d = L = 4$, $H_{\text{bal}} = 34.19\text{ bits}$) with private quadrant anchoring and non-zero offsets in $\mathbb{Z}_4 \times \mathbb{Z}_4 \setminus \{(0,0)\}$ ($\Omega = 32{,}760$; $|\mathcal{C}_0| = 131{,}040$).
- **Passive behavioral anomaly telemetry** (cognitive hesitation, pointer/touch kinematics, short-input cadence) bound to the active challenge identifier (`cid`).
- **Standards-compliant OpenID Connect Core 1.0 public-client profile** integrating RFC 7636 PKCE, registered RFC 8176 `amr` claims (`mfa`, `kba`, `rba`, `swk`), and RFC 9449 DPoP access token binding.

## Repository Structure

```text
.
├── main.tex                              # IEEEtran master LaTeX source
├── main.pdf                              # Compiled camera-ready PDF (10 pages)
├── references.bib                        # 40 authoritative peer-reviewed & normative citations
├── IEEEtran.cls                          # IEEE conference class
├── Proposta_TP2_Artigo_Cientifico_SSWM.md# Initial research paper proposal
├── sections/                             # Modular LaTeX sections (Abstract to Conclusion)
└── scripts/
    └── monte_carlo_intersection.py       # Reproducible Python 3 verification script (seed=2026)
```

## Reproducing All Mathematical & Simulation Results

No third-party dependencies are required (Python 3 standard library only):

```bash
python3 scripts/monte_carlo_intersection.py
```

This deterministically reproduces (`seed = 2026`):
- **Eq. (1):** Challenge matrix Shannon entropies ($34.19\text{ bits}$ quadrant-balanced, $55.45\text{ bits}$ half-balanced, $41.76\text{ bits}$ unconstrained multiset, $82.72\text{ bits}$ i.i.d.).
- **Fig. 3:** Worked toroidal matrix evaluation (`R_t = "M37K"`).
- **Table III:** 500-trial rational-adversary Monte Carlo intersection metrics (mean $\pm$ SD, median, $\text{P}_5$, $\text{P}_{95}$, and exact secret recovery rate $\Pr(|\mathcal{C}_k|=1)$).
- **Eq. (3):** Consecutive response divergence ($99.46\%$ fixed $\Sigma_{sub}$, $99.999\%$ resampled $\Sigma_{sub}$).

## Building the Paper

Using [Tectonic](https://tectonic-typesetting.github.io/) (XeTeX-based, reproducible TeX Gyre Times metrics):

```bash
tectonic main.tex
```

Or with standard `pdflatex` + `bibtex`:

```bash
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```
