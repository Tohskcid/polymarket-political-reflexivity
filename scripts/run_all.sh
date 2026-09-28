#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo "Master Replication Pipeline: Political Reflexivity Paper"
echo "=========================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "[Step 1/6] Verifying or acquiring raw data..."
python3 scripts/acquire/fetch_all_data.py

echo "[Step 2/6] Building processed analysis datasets..."
python3 scripts/clean/build_analysis_dataset.py

echo "[Step 3/6] Running data profiler for Table 1..."
python3 scripts/econ_data_profiler.py \
  --data data/processed/swing_states_panel.csv \
  --id state --time date --x poly_margin --y poll_margin \
  --latex --out-dir output/tables
# Ensure SVG is moved to output/figures
if [ -f output/tables/descriptive_binned_means_poll_margin_vs_poly_margin.svg ]; then
  mv output/tables/descriptive_binned_means_poll_margin_vs_poly_margin.svg output/figures/
fi

echo "[Step 4/6] Running econometric estimations and robustness checks (SVAR, VECM, Toda-Yamamoto, Local Projections, Panel FE, Event Dummies, Subsamples)..."
uv run --with scipy --with statsmodels --with matplotlib python3 scripts/analyze/estimate_models.py
uv run --with scipy --with statsmodels python3 scripts/analyze/robustness_checks.py

echo "[Step 5/6] Compiling academic manuscript into PDF..."
pdflatex -interaction=nonstopmode -output-directory=output/pdf paper/manuscript/main.tex > /dev/null
BIBINPUTS=.:paper/references:${BIBINPUTS:-} bibtex output/pdf/main > /dev/null
pdflatex -interaction=nonstopmode -output-directory=output/pdf paper/manuscript/main.tex > /dev/null
pdflatex -interaction=nonstopmode -output-directory=output/pdf paper/manuscript/main.tex > /dev/null
# Clean auxiliary LaTeX build files to maintain pristine layout
rm -f output/pdf/main.{aux,bbl,blg,log,out}

echo "[Step 6/6] Verifying research package and project layout gates..."
python3 scripts/check_data_provenance.py research/data-provenance.json --root . --json
python3 scripts/check_research_package.py --config research/package.json --root .
python3 scripts/check_project_layout.py --root . --json

echo "=========================================================="
echo "✅ Replication pipeline finished successfully!"
echo "Rendered PDF available at: output/pdf/main.pdf"
echo "=========================================================="
