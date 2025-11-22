# niivue-binder

niivue-binder

# Usage

Open the live demos with a web browser

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/neurolabusc/niivue-binder/HEAD?urlpath=lab/tree/notebooks/basic.ipynb)

# Development

You can work locally:

```bash
git clone https://github.com/neurolabusc/niivue-binder
cd niivue-binder
pip install -r requirements.txt
jupyter lab 
# open basic.ipynb notebook
```

# Committing

Jupyter notebooks cache a lot of meta data with each run. In addition, we try to keep the style of notebook scripts similar. Therefore, the following commands can clean up the notebooks if you wish to make a contribution to this repository:

```bash
python ./normalize_notebooks.py ./notebook
python -m ruff check ./notebooks/*.ipynb --fix
```