# btinference
Uses the inference3d module to infer the path of the bee in the photos

# Installation

You will need to install [pathinference](https://github.com/SheffieldMLtracking/pathinference), which requires tensorflow.
Example:

1) Install tensorflow (from [https://www.tensorflow.org/install/pip](tensorflow's page)):
```
python3 -m pip install 'tensorflow[and-cuda]'
pip install --upgrade tensorflow-probability
pip install tf-keras
```
2) then install pathinference,
```
pip install git+https://github.com/SheffieldMLtracking/pathinference.git
```
3) finally install this package:
```
pip install git+https://github.com/SheffieldMLtracking/btinference.git
```
If you want to render the path install:
```
sudo apt-get install ffmpeg
```

Or maybe just use this?

```
pip install opencv-python-headless
```

# Usage

Ran on server:
cd /mnt/san/shared/pml_group/Shared/beephotos/2025-09-09/Displacement_11
sudo btalignment . --maxnum 40 --calset cal

Then to view the results:
btqviewer . --nobrowser --port 5002 --highlight
Ran on my laptop:
ssh -N -L 5002:localhost:5002 sa_md1xmtsx@ohiobeeproject.sheffield.ac.uk
(then ran btqviewer on my laptop anywhere, just to open the right page in the browser, set port to 5002)

Because we have the non-compacted cal data in a different folder, after doing the alignment one needs to
copy the 'cal' folder (really it's just the cal/1010/
Ran on server:
sudo cp cal ../Displacement_11_compact/cal -r

Then cded to the right folder:
cd /mnt/san/shared/pml_group/Shared/beephotos/2025-09-09/Displacement_11_compact
sudo btinference --calset cal --makeanimation bee_1_compact
