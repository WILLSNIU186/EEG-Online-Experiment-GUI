# MRCP Online Interface (python)

Developed in University of Waterloo, Canada.
<br>
Contact Persons
<br>
Ning Jiang: n34jiang@uwaterloo.ca
<br>
Jiansheng Niu: j26niu@uwaterloo.ca

## Usage
This application is designed to communicate with most lab-streaming-layer(LSL) supported hardware
and to provide an experimental protocol equipped GUI for real-time data collection.
<br>
The basic communication with LSL is done by [1], this app expands the GUI to suit EEG/EMG/ECG experiments.

## Steps
1. Connect hardware with LSL driver or openvibe
2. Run this app and select the wanted stream in the terminal
3. GUI should show up and do your experiments!
 
## Installation

```buildoutcfg
cd lib\neurodecode-master
```
```buildoutcfg
python setup.py develop
```
```buildoutcfg
cd ..\..
```
```buildoutcfg
pip install -r requirements.txt
```
```buildoutcfg
python main.py
```

## Citation
[1] https://github.com/dbdq/neurodecode.git

