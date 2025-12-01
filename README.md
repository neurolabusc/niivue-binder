# niivue-binder

ipyniivue provides interactive visualization of medical volumes, meshes, streamlines, and connectomes in Jupyter. This repository includes recipes for [ipyniivue](https://github.com/niivue/ipyniivue) that can be run on the cloud using [mybinder](https://mybinder.org/v2/gh/neurolabusc/niivue-binder/HEAD?urlpath=lab/tree/notebooks/basic.ipynb) or locally from a jupyter notebook. See the [ipyniivue documentation](https://niivue.github.io/ipyniivue/) for more features.

## Usage: Binder

Open the live demos with a web browser using Binder. This is a zero-footprint solution: no files are downloaded to your computer. However, it does tend to be slow.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/neurolabusc/niivue-binder/HEAD?urlpath=lab/tree/notebooks/basic.ipynb)

## Usage: Colab

You can also paste notebook scripts into [Google Colab](https://colab.new/). Clone the repository and install dependencies. While this is less elegant than Binder, the performance is typically better.

```python
!git clone https://github.com/neurolabusc/niivue-binder
%cd niivue-binder
!pip install -q .

# Copy and paste a notebook, e.g. basic.ipynb

from ipyniivue import NiiVue

nv = NiiVue()
nv.load_volumes([{'path': './images/mni152.nii.gz'}])
nv
```

## Usage: Local

Working locally provides optimal performance. You have two options:

### Option A: pixi (recommended)

[pixi](https://pixi.sh/) provides fast, reproducible environments. Install pixi first, then:

```bash
git clone https://github.com/neurolabusc/niivue-binder
cd niivue-binder
pixi install
pixi run jupyter lab ./notebooks/basic.ipynb
```

### Option B: pip

If you prefer pip or already have a Python environment:

```bash
git clone https://github.com/neurolabusc/niivue-binder
cd niivue-binder
pip install .
jupyter lab ./notebooks/basic.ipynb
```

## Development

### Setup

```bash
git clone https://github.com/neurolabusc/niivue-binder
cd niivue-binder
pixi install
pixi run pre-commit install
```

### Environment Management

All environments use `pyproject.toml` as the source of truth:

| Environment | How It Works |
|-------------|--------------|
| **Local (pip)** | `pip install .` |
| **Local (pixi)** | `pixi install` (faster, uses conda-forge) |
| **Binder** | Uses `environment.yml` (auto-generated from pyproject.toml) |
| **Colab** | `pip install .` (Colab provides the notebook interface) |

**Workflow for updating dependencies:**

1. Edit `pyproject.toml` to add/update dependencies
2. Run `pixi install` to update your local environment
3. Commit - the pre-commit hook auto-generates `environment.yml`

> **Note:** `environment.yml` is auto-generated. Do not edit it directly.

### Code Quality

Pre-commit hooks automate code style, strip notebook outputs, and keep `environment.yml` in sync:

```bash
pixi run pre-commit run --all-files
```

### Running Tests

Execute notebooks to verify they work:

```bash
pixi run jupyter execute notebooks/*.ipynb
```
