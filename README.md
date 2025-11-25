# niivue-binder

ipyniivue provides interactive visualization of medical volumes, meshes, streamlines, and connectomes in Jupyter. This repository includes recipes for [ipyniivue](https://github.com/niivue/ipyniivue) that can be run on the cloud using [mybinder]((https://mybinder.org/v2/gh/neurolabusc/niivue-binder/HEAD?urlpath=lab/tree/notebooks/basic.ipynb)) locally from a jupyter notebook. See the [ipyniivue documentation](https://niivue.github.io/ipyniivue/) for more features.

# Usage

Open the live demos with a web browser

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/neurolabusc/niivue-binder/HEAD?urlpath=lab/tree/notebooks/basic.ipynb)

# Development

You can work locally:

```bash
git clone https://github.com/neurolabusc/niivue-binder
cd niivue-binder
pip install -r requirements.txt
jupyter lab ./notebooks/basic.ipynb
# press the 'run' button for the basic.ipynb notebook
```

# Committing

Jupyter notebooks cache a lot of meta data with each run. In addition, we try to keep the style of notebook scripts similar. Therefore, the following commands can clean up the notebooks if you wish to make a contribution to this repository:

```bash
python ./normalize_notebooks.py ./notebook
python -m ruff check ./notebooks/*.ipynb --fix
```