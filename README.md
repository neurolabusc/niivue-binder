# niivue-binder

ipyniivue provides interactive visualization of medical volumes, meshes, streamlines, and connectomes in Jupyter. This repository includes recipes for [ipyniivue](https://github.com/niivue/ipyniivue) that can be run on the cloud using [mybinder]((https://mybinder.org/v2/gh/neurolabusc/niivue-binder/HEAD?urlpath=lab/tree/notebooks/basic.ipynb)) locally from a jupyter notebook. See the [ipyniivue documentation](https://niivue.github.io/ipyniivue/) for more features.

# Usage: binder

Open the live demos with a web browser using binder. This is a zero-footprint solution: no files are downloaded to your computer. However, it does tend to be slow.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/neurolabusc/niivue-binder/HEAD?urlpath=lab/tree/notebooks/basic.ipynb)

# Usage: Colab

You can also paste notebook scripts into [Google Colab](https://colab.new/). You will want to make sure to clone the repository and install the requirements. While this is less elegant than binder, the performance is typically better. Here is a basic example:

```
!git clone https://github.com/neurolabusc/niivue-binder
%cd niivue-binder
!pip install -q -r requirements.txt

#copy and paste a notebook, e.g. basic.ipynb

from ipyniivue import NiiVue

nv = NiiVue()
nv.load_volumes([{'path': './images/mni152.nii.gz'}])
nv
```

# Usage: local and development

You can work locally, and this typically provides optimal performance. However, this does require considerable disk space:

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
python ./normalize_notebooks.py ./notebooks
python -m ruff check ./notebooks/*.ipynb --fix
```