# btinference
Uses the inference3d module to infer the path of the bee in the photos

# Installation

You will need to install [pathinference](https://github.com/SheffieldMLtracking/pathinference), which requires tensorflow.
Example:

1) Install tensorflow (from [https://www.tensorflow.org/install/pip](tensorflow's page)):
```
python3 -m pip install 'tensorflow[and-cuda]'
pip install --upgrade tensorflow-probability
```
2) then install pathinference,
```
pip install git+https://github.com/SheffieldMLtracking/pathinference.git
```
3) finally install this package:
```
pip install git+https://github.com/SheffieldMLtracking/btinference.git
```
