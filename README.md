# smart_tennis_2022 - tennis_tracker
## Description
使用真理大學架設高速相機所錄製影像進行網球落點偵測
<img src="./assert/tennis_tracking.gif" width="819" height="300"/>
## Requirements
- ubuntu = 18.04
- python = 3.6
- numpy = 1.19
- opencv_python = 4.1.2.30
- PIL = 8.4.0
- tifffile = 2020.9.5
- scipy = 1.5.4
- pykalman = 0.9.5
## Installation
1. Clone the repository
```
$ git clone https://github.com/rayhliu/smart_tennis_2022-tennis_tracking.git
```
2. Install python package
```
$ pip install -r requirement.txt
```
## Usage
#### 1. Run tennis_calibration_app.py
get tennis court calibration parameters json file
```
python ./tennis_calibration_app.py [-h][-d FRAME_DIR]
                                   [-o PARAM_OUTPUTPATH]
# example
python ./tennis_calibration_app.py -d dataset/cam_1_20220920_153428
```
#### 2. Run tennis_tracker_app.py
```
python ./tennis_tracker_app.py [-h][-p PARAM_PATH][-d FRAME_DIR]
                               [-s SHOW_INFO][-sv SAVE_VIDEO]
# example
python ./tennis_tracker_app.py -p ./assert/court_left_parameters.json -s -sv
```
