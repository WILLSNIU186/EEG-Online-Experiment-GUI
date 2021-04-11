# EEG online experiment GUI

## Description

This is a GUI designed for EEG data online collection and experiment. Most commercial EEG 
instruments such as NeuroElectric, Gtec and BrainProducts are compatible with this GUI as 
long as they are supported by [lab streaming layer (LSL)](https://labstreaminglayer.readthedocs.io/info/supported_devices.html) . The basic communication with LSL is done by [1], 
this app expands the GUI to suit EEG/EMG/ECG experiments.

This GUI provides experimenters a ready-togo platform with following functions:
1. Recording
2. Experiment protocol DIY
3. Online feedback for experimenter
    1. EEG signal online visualization
    2. Interested signal extraction and visualization 
    3. Bad trial monitor
4. Online feedback for subject
    1. Task image
    2. Task sound
<br>

![Alt text](docs/tutorial_images/Exp_record.png?raw=true)


# Getting Started


## [Installation](https://willsniu186.github.io/uw_eboinics_experimental_interface/build/html/Installation_and_setup.html)


## [Tutorial](https://willsniu186.github.io/uw_eboinics_experimental_interface/build/html/Tutorial.html)


## Steps
1. Connect hardware with LSL driver or openvibe
2. Run this app and select the wanted stream in the terminal
3. GUI should show up and do your experiments!


## Contact
Jiansheng Niu: jiansheng.niu1@uwaterloo.ca
<br>
Dr. Ning Jiang: ning.jiang@uwaterloo.ca

_Developed in University of Waterloo, Canada._
## Citation
[1] https://github.com/dbdq/neurodecode.git

