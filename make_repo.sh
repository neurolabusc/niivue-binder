#!/usr/bin/env bash
set -euo pipefail
repo_dir="${1:-ipyniivue-binder-demo}"
echo "Creating repo in: $repo_dir"
mkdir -p "$repo_dir"
cd "$repo_dir"

# Create directories
mkdir -p notebooks images .github/workflows scripts

# requirements
cat > requirements.txt <<'REQ'
ipyniivue
notebook
jupyterlab
ipywidgets
voila
nbconvert
matplotlib
numpy
REQ

# README with Binder + Colab instructions
cat > README.md <<'MD'
# ipyniivue Binder demo repo (minimal)

This repository contains two example notebooks demonstrating `ipyniivue`:
- `notebooks/basic.ipynb` — minimal usage (renders a single volume)
- `notebooks/timeseries.ipynb` — 4D timeseries example with an `ipywidgets` slider

**How to run on Binder**
Click the Binder link (replace `<user>` and `<repo>` with your GitHub user and repository name after pushing):
`https://mybinder.org/v2/gh/<user>/<repo>/<branch>?filepath=notebooks%2Fbasic.ipynb`

Binder will build the environment using `requirements.txt`. Make sure `ipyniivue` is in `requirements.txt` (it is). The notebooks download example images from `https://niivue.com/demos/images/` at runtime, so you do not need to commit large binaries.

**Open in Colab**
You can also open the notebooks in Colab:
`https://colab.research.google.com/github/<user>/<repo>/blob/<branch>/notebooks/basic.ipynb`

MD

# .gitignore
cat > .gitignore <<'GI'
__pycache__/
.ipynb_checkpoints/
out/
images/*.nii.gz
GI

# scripts (empty for now)
cat > scripts/README.md <<'S'
Helper scripts (none required for this minimal demo).
S

# simple GitHub Actions workflow to convert notebooks to HTML and publish to gh-pages (optional)
cat > .github/workflows/build-gh-pages.yml <<'YAML'
name: Build notebooks to gh-pages
on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Convert notebooks to HTML
        run: |
          mkdir -p out
          jupyter nbconvert notebooks/basic.ipynb --to html --output out/basic.html
          jupyter nbconvert notebooks/timeseries.ipynb --to html --output out/timeseries.html
      - name: Deploy to gh-pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./out
YAML

echo "Repo skeleton created. Edit README.md to replace <user>/<repo>/<branch> with your values."
