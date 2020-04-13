# SylviesFitnessCircuit

SylviesFitnessCicuit (SFCircuit.py) provides a python-based circuit training exercise program to perform at home alone or together with your friends.

The core of the program is based on the pysimplegui cookbook [pysimplegui_cookbook](https://pysimplegui.readthedocs.io/en/latest/cookbook/) and the demo program WidgetTimer: 
[pysimplegui_timer](https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Desktop_Widget_Timer.py)


## Installation and Usage

Clone repository. Navigate in the terminal to the folder SylviesFitnessCircuit. Run via the command line: python SFCircuit.py 

### Gui Navigation

The GUI can be navigated by clicking the buttons. The Choose workout window has the option to A) choose a Pre-set workout, B) use the Surprise Button (which chooses 12 exercised radomly from a list) or C) pick as many exercise of "Your Choice" as you want. In the next window, you pick the Duration and frequency of the workouts. It also shows you a list of the selected workouts. You can pick again, if you want to choose a different set. If you change the Nr of Workouts after picking "Surprise" to fewer workouts, the number of workouts will be reduced and cut off at the bottom. First, an introduction timer will go through the different exercises, which can be skipped if needed. Subsequently, a warm up section will go through 6 different exersices, which can only be change within the script. The beginning and end of an exercise is accompanied by a sound signal (Default in script = 1 = Sound on).


### Script Navigation
For now, lists of different workouts are accessible within the script. A Pre-Set Workout List can be modified within the script or chosen within the GUI (randomly “Surprise” or by “Your Choice”).  

WORKOUT and WARMUP LIST can be modified within the script.


* Python 3.6
* pysimplegui
* simpleaudio

![Logo-Banner](LogoSFC/Logo-Banner-1-01.png)
