#!/usr/bin/env python
import PySimpleGUI as sg
import time
import simpleaudio as sa
import random
import math
import os

"""
SylviesFitnessCicuit (SFC) is based and modified from https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Desktop_Widget_Timer.py
This scripts provides a circuit training-based exercise program. 
You can modifie the Pre-Set WORKOUT LIST within the script or choose randomly assigned workouts ('Surprise') or choose from 
the exercise list provided in the script ('Your Choise'). 
WORKOUT and WARMUP LIST can be modified within the script.
Duration and frequency of workouts can be changed within the GUI.

"""

"""
 Timer Desktop Widget Creates a floating timer that is always on top of other windows 
 You move it by grabbing anywhere on the window Good example of how to do a non-blocking, polling program using PySimpleGUI 
 Something like this can be used to poll hardware when running on a Pi
 While the timer ticks are being generated by PySimpleGUI's "timeout" mechanism, the actual value
  of the timer that is displayed comes from the system timer, time.time().  This guarantees an
  accurate time value is displayed regardless of the accuracy of the PySimpleGUI timer tick. If
  this design were not used, then the time value displayed would slowly drift by the amount of time
  it takes to execute the PySimpleGUI read and update calls (not good!)
"""



def time_as_int():
    return int(round(time.time() * 100))

####### PARAMETERS THAT CAN/HAVE TO BE MODIFIED #####
Hydrate = 60*100
K=6 #number of warm up workouts
#COOSE MUSIC FOR BEGINNING OF WORK, REST ETC (.WAV FILE NEEDS TO BE IN SAME FOLDER AS SCRIPT)

SoundWork = os.path.join('Sounds','Air Horn-SoundBible.com-964603082.wav')
SoundRest = os.path.join('Sounds','Bike Horn-SoundBible.com-602544869.wav')
#SoundRest = "beep09.wav"
soundon = (1)  #0 = sound off, 1 == sound on  

###### Style ###
FontTimer = 80
FontWorkOut = 56
WidthTime = 9 #8
WidthWorkOut = 12 #11
######## font sizes for guis ####### 
SizeWork = 24
FontText = 16


###### WORKOUT LIST
#WarmUpList = ('Burpees','Roll Backwards + strech forward','Glute bridge',  '10 Mountain Climber, 3 Push Up', 'Star Jump', 'High Knees and Air Punches') 
WarmUpList = ('Burpees','5 shoulder circles + 2 wind mills','Glute bridge', 'Squat Pulses', 'Single Leg Hip Circles', 
              'Jumping Jacks') 
#'Back stretch (turn leg over side)'
ListBelly = ('Sit up','Crunches', 'Jack Knife', 'Bicycle Crunches', 'Russian Twist','Heel Touch Crunches','Leg Lift & Hold') #Windshield Wiper

ListLeg = ('Wall Sit (alt: Squat)', 'Rope Jumps',  'Ice Skater', 'Ladder (alt: Fast Feet)', '10 Fast Feet + Jump','Squat',
           'Frog Squats', 'Hurdles','Jumping Lunges (Plyo)','High Knee and Tuck Jumps', 'Sumo Squat',
            'Sumo Squat (+ Touch)','Squat Walk', 'Backward Lunge', '6 Fast Feet In & Out', '2 Squats, 2 Squat Jumps','Jump + Squat Backwards', 
            'Side Lunges', 'Inner Sole Taps')

ListRest = ('Mountain Climber', 'Push Ups','Burpees','Pull Ups (alt: Superman)', 'Plank', 'Shoot through', 'Low + High Plank Switch',
            'Swimmer', 'Diamond Push Up', 'Spiderman Push Up', 'Inch Worm', 'Bear Crawl','Jumping Jacks',
            'Single-Leg Glute Bridge','4 Sprawl + 2 Push Up', 'Jump + Donkey Kick (n+1)','Push Up + Side Turn', 'Mount. Climb. Side Step',
            'Bird Dog','Side Plank + elev. leg', 'Tricep Dips', 'Star Push Up Jump', 'Burpee + Jump 180','Prayer Pulse')


 #'Medicine ball twist',' 'medicine ball Slam', 'Box jump', 'Ketttlebell swing',
#Donkey Jump

AllWO = ListBelly + ListLeg + ListRest
AllWO = list(AllWO)




#######################################################3 Welcome window and wait for next workout ##############################
sg.theme('DarkTeal2')
layoutWelcome = [[sg.Text('')],
          [sg.Text('Welcome to SFC - Sylvie\'s Fitness Circuit', size=(42, 1), font=('Helvetica', FontWorkOut),
                justification='center')],
    [sg.Text('!!! Let\'s work out together !!!', size=(42, 1), font=('Helvetica', FontWorkOut),
                justification='center')],
     [sg.Text('I am not a certified trainer. Please consult a personal trainer for advice on the exercise. ', size=(76, 1), font=('Helvetica', FontWorkOut-24),
                justification='center')],
     [sg.Text('Do the exercise on your own pace. There is no winning, no losing, just fun !', size=(74, 1), font=('Helvetica', FontWorkOut-24),
                justification='center')],
                    [sg.Text('', size=(36, 1), font=('Helvetica', FontWorkOut+10),
                justification='center', key='-Welcome-')],
        [sg.Button('Pause', key='-RUN-PAUSE-', button_color=('white', '#001480')),
           #sg.Button('Reset', button_color=('white', '#007339'), key='-RESET-'),
        sg.Button('Skip', button_color=('white', '#f5a70c'), key='-Skip-'),
         sg.Exit(button_color=('white', 'firebrick4'), key='-RealExit-')]]
#
windowWelcome = sg.Window('Welcome to SFC', layoutWelcome,
                   auto_size_buttons=False,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0),
                   location=(20, 100)) 
########

current_time, paused_time, paused = 0, 0, False
start_timeWelcome = time_as_int()
WelcomeCD = 120*100
TimeDownWelcome = WelcomeCD
  
#while True:
while (TimeDownWelcome > 0):   # print('I am here')
    # --------- Read and update window --------
    if not paused:
        event, values = windowWelcome.read(timeout=10)
        current_time = (time_as_int() - start_timeWelcome)
        TimeDownWelcome = WelcomeCD - current_time
    else:
        event, values = windowWelcome.read()
    # --------- Do Button Operations --------
    if event in (None, '-Skip-'):        # ALWAYS give a way out of program
        break
    if event in '-RealExit-':
        exit()
    if event == '-RESET-':
        paused_time = start_timeWelcome = time_as_int()
        current_time = 0
    elif event == '-RUN-PAUSE-':
        paused = not paused
        if paused:
            paused_time = time_as_int()
        else:
            start_timeWelcome = start_timeWelcome + time_as_int() - paused_time
        # Change button's text
        windowWelcome['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
        
    # --------- Display timer in window --------
#            windowWU['Warmup'].update('{:02d}:{:02d}.{:02d}'.format((TimeDownWU // 100) // 60,
#                                                                (TimeDownWU // 100) % 60,
#                                                                TimeDownWU % 100))   
 
    windowWelcome['-Welcome-'].update('{:02d}:{:02d}'.format((TimeDownWelcome  // 100) // 60,
                                                        (TimeDownWelcome // 100) % 60)) 

windowWelcome.close()
#########



########################################################  Choose the Length of the workout #########

#LengthWorkoutBy5 =  MAKE IT FLEXIBLE FOR THE LENGTH OF THE LIST

eventChooseTime = 'Pick Again'

while eventChooseTime != 'Start':
    
    sg.theme('LightBlue3')
     
    AllWO_regrouped = []
    n = 0
    for x in range(0,math.ceil(len(AllWO)/5)):  ##### Nr of WO 47. make it flexible or add more WO :)
        innerlist = []
        for i in range(5):
            innerlist.append(sg.Checkbox(AllWO[n], size=(SizeWork, 1), font=('Helvetica', FontText)))
            n = n+1
        AllWO_regrouped.append(innerlist)
        
 
    layoutChoose = [[sg.Text('')],
                     ######## chose workout
                     [sg.Text('Choose workouts', size=(34, 1), font=('Helvetica', 28))],
                    [sg.Text('',font=('Helvetica', 2))]]
    
    ButtonsLayOut = [[sg.Text('',font=('Helvetica', 2))], 
                     [sg.Button('Pre-set',  font=('Helvetica', FontText)),
                      sg.Text(''),
                      sg.Button('Surprise',  font=('Helvetica', FontText)),
                      sg.Text(''),
                      sg.Button('Your Choice',  font=('Helvetica', FontText)),
                      sg.Text(''),
                      sg.Exit( font=('Helvetica', FontText)),
                      sg.Text('')]]
    
    
    for k in range(0,len(AllWO_regrouped)):
        layoutChoose.append(AllWO_regrouped[k]) 
        
         
    for l in range(0,len(ButtonsLayOut)):
        layoutChoose.append(ButtonsLayOut[l]) 
       
    
    windowChoose= sg.Window('choose your workout', layoutChoose,
                       auto_size_buttons=False,
                       keep_on_top=True,
                       grab_anywhere=True,
                       element_padding=(0, 0),
                       location=(100, 100)) 
    
    
    eventChoose, valueWO = windowChoose.read()  
      
    windowChoose.close()
    
    
    #eventChoose = StartPick()  
     #   return valueWO
        
    if eventChoose in ['Exit']:
        exit()
    
    ListofBoolWO = []
    for WOlist in range(0, len(valueWO)):
        #print(valueTimes[WOlist])
        if valueWO[WOlist] == True or valueWO[WOlist] == False:    #type('bool')???
            ListofBoolWO.append(valueWO[WOlist])
            
    #print(ListofBoolWO)        
       
    
    NewWOList = []
    for x in range (0, len(ListofBoolWO)):
        if ListofBoolWO[x] == True:
            NewWOList.append(AllWO[x])
            
#    print(NewWOList)   
#    print(len(NewWOList))    
#    print(eventChoose)
    ################################################# Choose or create workout list ###########################################
    
    if eventChoose in ['Pre-set']:
        
    ###################### Pre-Set WORKOUT LIST #######3
        WorkoutList = ('Sumo Squat (+ Touch)', 'Sit up','Swimmer',
                       'Inner Sole Taps', 'Bicycle Crunches', '10 Fast Feet + Jump', 
                       '4 Sprawl + 2 Push Up',  'Bear Crawl','Jack Knife', 'Wall Sit', 
                       'Single-Leg Glute Bridge', 'Jump + Squat Backwards')

 
    elif eventChoose in ['Your Choice']:
    ###################### TODAY's PICK WORKOUT LIST #######3
        random.shuffle(NewWOList)
        WorkoutList = NewWOList
        #print(len(WorkoutList))
     
    elif eventChoose in ['Surprise']:
        random.shuffle(AllWO)
        WorkoutList = AllWO
        #print(len(WorkoutList))
       
    else:# change or can be deleted    
        WorkoutList = AllWO
        
    #print(type(AllWO))
    print(WorkoutList)          

    ######################### Window choose time interval for workouts and show which workout choosen   #######
    
    
    #### length of workout that will be displayed (set for suprise = 12, as the randomiztion is one on AllWO listm which contains all workouts)
    NrWOdefault =[]
    if eventChoose in ['Your Choice']:
        NrWOdefault  = len(WorkoutList)
        
    elif eventChoose in ['Pre-set']:   
        NrWOdefault  = len(WorkoutList)
        
    else:
        NrWOdefault  = 12
    
    
    WorkoutListShow = list(WorkoutList)
    
    
    if eventChoose in ['Surprise']:
        LengthWO = 12
    else:
        LengthWO = len(WorkoutListShow)
    
    ShowChosenWO = []     
    n = 0
    for x in range(LengthWO):  
        innerlist2 = []
        for i in range(1):
            innerlist2.append(sg.Checkbox(WorkoutListShow [n], size=(SizeWork, 1), font=('Helvetica', FontText)))
            n = n+1
        ShowChosenWO.append(innerlist2)
        
    
    
    ### default values for Work out time, Rest time etc are entered here
    sg.theme('LightBlue3')
    layoutChooseTime = [[sg.Text('')],
              [sg.Text('Choose Timing', size=(16, 1), font=('Helvetica', 28))],
                    [sg.Text('',font=('Helvetica', 2))],
                     [sg.Text('Enter Work Out Time (s)',font=('Helvetica', FontText)),sg.InputText('35', size=(6,1),
                      justification='center', font=('Helvetica', FontText))],
                     [sg.Text('',font=('Helvetica', 2))],
                     [sg.Text('Enter Rest Time (s)', font=('Helvetica', FontText)),sg.InputText('10', size=(6,1),
                     justification='center', font=('Helvetica', FontText))],
                     [sg.Text('',font=('Helvetica', 2))],
                     [sg.Text('Enter Nr of Workouts',font=('Helvetica', FontText)),sg.InputText(NrWOdefault, size=(6,1),justification='center',
                      font=('Helvetica', FontText))],
                     [sg.Text('',font=('Helvetica', 2))],
                     [sg.Text('Enter Nr of Repeats',font=('Helvetica', FontText)),sg.InputText('3', size=(6,1),justification='center',
                      font=('Helvetica', FontText))],
                     [sg.Text('',font=('Helvetica', 2))],
                     #[sg.Text('Enter Warm Up Time (Workouts)',font=('Helvetica', FontText)),sg.InputText('25', size=(6,1),justification='center',
                      #font=('Helvetica', FontText))],
                    [sg.Text('',font=('Helvetica', 2))],
                    [sg.Text('Todays Workout: ', size=(16, 1), font=('Helvetica', 28))],
                    [sg.Text('',font=('Helvetica', 2))]]
    
    ButtonsLayOut2 = [[sg.Text('',font=('Helvetica', 2))], 
                     [sg.Button('Start',  font=('Helvetica', FontText)),
                      sg.Text(''),
                      sg.Button('Pick Again',  font=('Helvetica', FontText)),
                      sg.Text(''),
                      sg.Exit( font=('Helvetica', FontText)),
                      sg.Text('')]]
    
    
    for k in range(0,len(ShowChosenWO)):
        layoutChooseTime.append(ShowChosenWO[k]) 
        
        
    for l in range(0,len(ButtonsLayOut2)):
        layoutChooseTime.append(ButtonsLayOut2[l]) 
        
    
    windowChooseTime = sg.Window('choose your workout duration', layoutChooseTime,
                       auto_size_buttons=False,
                       keep_on_top=True,
                       grab_anywhere=True,
                       element_padding=(0, 0),
                       location=(100, 100)) 
    
    eventChooseTime, valueTimes = windowChooseTime.read()  
    
    windowChooseTime.close()   

#    print(eventChooseTime)
#    print(type(eventChooseTime))
    
    if eventChooseTime in ['Exit']:
        exit()


##################################################
###################################3   WORKOUT REST AND HYDRATE TIMER TIMES CHOSEN FROM THE WINDOW ABOVE
Work = int(valueTimes[0])*100
WorkWU = 25*100 #int(valueTimes[4])*100
Rest = int(valueTimes[1])*100


#CHoose Number of workouts and repetions (enter in window above)
gesamt = int(valueTimes[3])  #number of repetions
NrofWorkouts = int(valueTimes[2])





################################################   INTRO ###########################################

##### Introduce WorkOut ####
sg.theme('LightBlue3')
layoutIntroWork = [[sg.Text('')],
                [sg.Text('Intro Workouts', size=(WidthWorkOut, 1), font=('Helvetica', FontWorkOut),
                justification='center')],
          [sg.Text('', size=(WidthTime, 1), font=('Helvetica', FontTimer),
                justification='center', key='-IntroWork-')],
            [sg.Text('', size=(WidthWorkOut, 3), font=('Helvetica', FontWorkOut),
                justification='center', key='workout')],
          [sg.Button('Pause', key='-RUN-PAUSE-', button_color=('white', '#001480')),
           #sg.Button('Reset', button_color=('white', '#007339'), key='-RESET-'),
        sg.Button('Next', button_color=('white', '#007339'), key='-Next-'),
           sg.Button('Skip', button_color=('white', '#f5a70c'), key='-Skip-'),                             
         sg.Exit(button_color=('white', 'firebrick4'), key='-RealExit-')]]
#
windowIntroWork = sg.Window('Introduction of Workout', layoutIntroWork,
                   auto_size_buttons=False,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0),
                   location=(100, 100))    

IntroWork = 12*100
intro = NrofWorkouts


while (intro>0):
#while (intro):    
    #print(n)
        #sg.one_line_progress_meter('My Meter', NrofWorkouts-intro, NrofWorkouts-1, 'key', orientation="h")        
        intro= intro-1
        current_time, paused_time, paused = 0, 0, False
        start_timeIntroWork= time_as_int()
        TimeDownIntroWork = IntroWork
      
        #while True:
        while (TimeDownIntroWork > 0):   # print('I am here')
            # --------- Read and update window --------
            if not paused:
                event, values = windowIntroWork.read(timeout=10)
                current_time = (time_as_int() - start_timeIntroWork)
                TimeDownIntroWork = IntroWork- current_time
            else:
                event, values = windowIntroWork.read()
            # --------- Do Button Operations --------
            if event in (None, '-Next-'):        # ALWAYS give a way out of program
                break
            if event in '-RealExit-':
                exit()
            if event in '-Skip-':
                windowIntroWork.close()
            if event == '-RESET-':
                paused_time = start_timeIntroWork = time_as_int()
                current_time = 0
            elif event == '-RUN-PAUSE-':
                paused = not paused
                if paused:
                    paused_time = time_as_int()
                else:
                    start_timeIntroWork = start_timeIntroWork + time_as_int() - paused_time
                # Change button's text
                windowIntroWork['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
                
            # --------- Display timer in window --------
            windowIntroWork['-IntroWork-'].update('{:02d}:{:02d}'.format((TimeDownIntroWork // 100) // 60,
                                                                (TimeDownIntroWork // 100) % 60))   
          
    
            windowIntroWork['workout'].update(WorkoutList[intro]) 
            

            
windowIntroWork.close()



#######################################################3 Get READY To WARM UP  ##############################
sg.theme('DarkRed1')
layoutGetReady = [[sg.Text('')],
          [sg.Text('Get Ready to warm up', size=(20, 1), font=('Helvetica', FontTimer),
                justification='center', key='-delete-')],
                [sg.Text('', size=(20, 1), font=('Helvetica', FontTimer),
                justification='center', key='-getready-')],
        [sg.Button('Pause', key='-RUN-PAUSE-', button_color=('white', '#001480')),
           #sg.Button('Reset', button_color=('white', '#007339'), key='-RESET-'),
        sg.Button('Next', button_color=('white', '#007339'), key='-Next-'),
         sg.Exit(button_color=('white', 'firebrick4'), key='-RealExit-')]]
#
windowGetReady = sg.Window('Get Ready', layoutGetReady,
                   auto_size_buttons=False,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0),
                   location=(100, 100)) 
###########

current_time, paused_time, paused = 0, 0, False
start_timeReady = time_as_int()
ReadyCD = 5*100
TimeDownReady = ReadyCD 
  
#while True:
while (TimeDownReady > 0):   # print('I am here')
    # --------- Read and update window --------
    if not paused:
        event, values = windowGetReady.read(timeout=10)
        current_time = (time_as_int() - start_timeReady)
        TimeDownReady = ReadyCD - current_time
    else:
        event, values = windowGetReady.read()
    # --------- Do Button Operations --------
    if event in (None, '-Next-'):        # ALWAYS give a way out of program
        break
    if event in '-RealExit-':
        exit()
    if event == '-RESET-':
        paused_time = start_timeReady = time_as_int()
        current_time = 0
    elif event == '-RUN-PAUSE-':
        paused = not paused
        if paused:
            paused_time = time_as_int()
        else:
            start_timeReady = start_timeReady + time_as_int() - paused_time
        # Change button's text
        windowGetReady['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
        
    # --------- Display timer in window --------
#            windowWU['Warmup'].update('{:02d}:{:02d}.{:02d}'.format((TimeDownWU // 100) // 60,
#                                                                (TimeDownWU // 100) % 60,
#                                                                TimeDownWU % 100))   
 
    windowGetReady['-getready-'].update('{:02d}:{:02d}'.format((TimeDownReady  // 100) // 60,
                                                        (TimeDownReady // 100) % 60)) 

windowGetReady.close()
#########

##############################################   WARM UP TIMER ################################
  
#### Warm up timer
sg.theme('DarkBlue4')
layoutWU = [[sg.Text('')],
              [sg.Text('Warm Up', size=(WidthWorkOut, 1), font=('Helvetica', FontWorkOut),
                justification='center')],
          [sg.Text('', size=(WidthTime, 1), font=('Helvetica', FontTimer),
                justification='center', key='Warmup')],
            [sg.Text('', size=(WidthWorkOut, 3), font=('Helvetica', FontWorkOut),
                justification='center', key='workout')],
          [sg.Button('Pause', key='-RUN-PAUSE-', button_color=('white', '#001480')),
           #sg.Button('Reset', button_color=('white', '#007339'), key='-RESET-'),
        sg.Button('Next', button_color=('white', '#007339'), key='-Next-'),
        sg.Button('Skip', button_color=('white', '#f5a70c'), key='-Skip-'),
         sg.Exit(button_color=('white', 'firebrick4'), key='-RealExit-')]]
#
windowWU = sg.Window('Warm Up 2 min', layoutWU,
                   auto_size_buttons=False,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0),
                   location=(400, 100))    


######## WARM UP
while (K>0):
    #print(n)
        K = K-1
        current_time, paused_time, paused = 0, 0, False
        start_timeWU = time_as_int()
        TimeDownWU = WorkWU 
      
        #while True:
        while (TimeDownWU > 0):   # print('I am here')
            # --------- Read and update window --------
            if not paused:
                event, values = windowWU.read(timeout=10)
                current_time = (time_as_int() - start_timeWU)
                TimeDownWU = WorkWU - current_time
            else:
                event, values = windowWU.read()
            # --------- Do Button Operations --------
            if event in (None, '-Next-'):        # ALWAYS give a way out of program
                break
            if event in '-RealExit-':
                exit()
            if event in '-Skip-':
                windowWU.close()
                K = 0
            if event == '-RESET-':
                paused_time = start_timeWU = time_as_int()
                current_time = 0
            elif event == '-RUN-PAUSE-':
                paused = not paused
                if paused:
                    paused_time = time_as_int()
                else:
                    start_timeWU = start_timeWU + time_as_int() - paused_time
                # Change button's text
                windowWU['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
                
            # --------- Display timer in window --------
#            windowWU['Warmup'].update('{:02d}:{:02d}.{:02d}'.format((TimeDownWU // 100) // 60,
#                                                                (TimeDownWU // 100) % 60,
#                                                                TimeDownWU % 100))   
 
            windowWU['Warmup'].update('{:02d}:{:02d}'.format((TimeDownWU // 100) // 60,
                                                                (TimeDownWU // 100) % 60))  
             #######  END OF EXERCISE START OF REST

                          
            windowWU['workout'].update(WarmUpList[K]) 
            
        if soundon == 1:       
            wave_obj = sa.WaveObject.from_wave_file(SoundRest)
            play_obj = wave_obj.play()
            play_obj.wait_done()
        
windowWU.close()


###################################### ###################  Get READY TO WORK OUT ######
sg.theme('DarkRed1')
layoutGetReadyWork = [[sg.Text('')],
          [sg.Text('Get Ready to work out', size=(20, 1), font=('Helvetica', FontTimer),
                justification='center', key='-delete-')],
                [sg.Text('', size=(20, 1), font=('Helvetica', FontTimer),
                justification='center', key='-getready-')],
        [sg.Button('Pause', key='-RUN-PAUSE-', button_color=('white', '#001480')),
        sg.Button('Next', button_color=('white', '#007339'), key='-Next-'),
         sg.Exit(button_color=('white', 'firebrick4'), key='-RealExit-')]]
#
windowGetReadyWork = sg.Window('Get Ready', layoutGetReadyWork,
                   auto_size_buttons=False,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0),
                   location=(100, 100)) 
###########

current_time, paused_time, paused = 0, 0, False
start_timeReady = time_as_int()
ReadyCD = 5*100
TimeDownReady = ReadyCD 
  
#while True:
while (TimeDownReady > 0):   # print('I am here')
    # --------- Read and update window --------
    if not paused:
        event, values = windowGetReadyWork.read(timeout=10)
        current_time = (time_as_int() - start_timeReady)
        TimeDownReady = ReadyCD - current_time
    else:
        event, values = windowWU.read()
    # --------- Do Button Operations --------
    if event in (None, '-Next-'):        # ALWAYS give a way out of program
        break
    if event in '-RealExit-':
        exit()
    if event == '-RESET-':
        paused_time = start_timeReady = time_as_int()
        current_time = 0
    elif event == '-RUN-PAUSE-':
        paused = not paused
        if paused:
            paused_time = time_as_int()
        else:
            start_timeReady = start_timeReady + time_as_int() - paused_time
        # Change button's text
        windowGetReadyWork['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
        

    windowGetReadyWork['-getready-'].update('{:02d}:{:02d}'.format((TimeDownReady  // 100) // 60,
                                                        (TimeDownReady // 100) % 60)) 

windowGetReadyWork.close()

##########################################  WORKOUT + REST and HYDRATE ##############
#sg.theme('DarkPurple5')
#sg.theme('DarkBlue5')
final = NrofWorkouts * gesamt
sg.theme('DarkRed1')
layout = [[sg.Text('')],
          [sg.Text('', size=(WidthTime, 1), font=('Helvetica', FontTimer),
                justification='center', key='text')],
            [sg.Text('', size=(WidthWorkOut, 4), font=('Helvetica', FontWorkOut),
                justification='center', key='workout')],
          [sg.Button('Pause', key='-RUN-PAUSE-', button_color=('white', '#001480')),
        sg.Button('Next', button_color=('white', '#007339'), key='-Next-'),
         sg.Exit(button_color=('white', 'firebrick4'), key='-RealExit-')],
            [sg.Text('',font=('Helvetica', 2))],
            [sg.Text('Progress',font=('Helvetica', FontWorkOut-25))],
            #[sg.Text('Progress', size=(35, 20), font=('Helvetica', FontWorkOut-25),
             #   justification='center')],
          [sg.ProgressBar(NrofWorkouts, orientation='h', size=(35, 20), key='-progressbar-')],
                       [sg.Text('',font=('Helvetica', 2))],
           [sg.Text('Progress Laps',font=('Helvetica', FontWorkOut-25))],
            [sg.ProgressBar(final, orientation='h', size=(35, 20), key='-progressbargesamtWork-')]]

window = sg.Window('Work Time', layout,
                   auto_size_buttons=False,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0),
                   location=(10, 200))


##### theme Rest 

sg.theme('Black')
layout2 = [[sg.Text('')],
          [sg.Text('', size=(WidthTime, 1), font=('Helvetica', FontTimer),
                justification='center', key='text2')], 
         [sg.Text('REST', size=(WidthWorkOut, 1), font=('Helvetica', FontWorkOut),
                justification='center', key='-rest-')],
         [sg.Text('', size=(WidthWorkOut, 3), font=('Helvetica', FontWorkOut),
                justification='center', key='-upnext-')],           
          [sg.Button('Pause', key='-RUN-PAUSE-', button_color=('white', '#001480')),
           sg.Button('Next', button_color=('white', '#007339'), key='-Next-'),
            sg.Exit(button_color=('white', 'firebrick4'), key='-RealExit-')],
            [sg.Text('',font=('Helvetica', 2))],
            [sg.Text('Progress',font=('Helvetica', FontWorkOut-25))],
            [sg.ProgressBar(NrofWorkouts, orientation='h', size=(35, 20), key='-progressbarRest-')],
             [sg.Text('',font=('Helvetica', 2))],
           [sg.Text('Progress Laps',font=('Helvetica', FontWorkOut-25))],
            [sg.ProgressBar(final, orientation='h', size=(35, 20), key='-progressbargesamt-')]]
 
window2 = sg.Window('Rest', layout2,
                   auto_size_buttons=False,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0),
                   location=(10, 200))


# int(valueTimes[2])-1  
# WorkoutList[int(valueTimes[2])-1]
##### theme Hydrate 
sg.theme('DarkBlue10')         
layout3 = [[sg.Text('')],
          [sg.Text('', size=(WidthTime, 1), font=('Helvetica', FontTimer),
                justification='center', key='text3')],
      [sg.Text('WATER REFILL', size=(WidthWorkOut,3), font=('Helvetica', FontWorkOut),
                justification='center', key='-HYDRATE2-')],
               # [sg.Text('up next: ', size=(WidthWorkOut, ), font=('Helvetica', FontWorkOut),
               # justification='center', key='-WOafterBreak-')],
            [sg.Text('Up next:  '+ WorkoutList[int(valueTimes[2])-1], size=(WidthWorkOut,3), font=('Helvetica', FontWorkOut),
                justification='center', key='-HYDRATE-')],         
          [sg.Button('Pause', key='-RUN-PAUSE-', button_color=('white', '#001480')),
           sg.Button('Next', button_color=('white', '#007339'), key='-Next-'),
            sg.Exit(button_color=('white', 'firebrick4'), key='-RealExit-')]]          
          
window3 = sg.Window('Hydrate', layout3,
                   auto_size_buttons=False,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0),
                   location=(450, 200))



######################################### WORKOUT TIMER STARTS HERE
lowerProgress  = 0
while (gesamt>0):
    n = NrofWorkouts # number of workouts
    gesamt = gesamt-1
    
    
    while (n>0):
    #print(n)
        #lowerProgress  = lowerProgress  + 1
        final = final-1
        n = n-1
        current_time, paused_time, paused = 0, 0, False
        start_time = time_as_int()
        TimeDown = Work
        TimeDownRest = Rest


        if soundon == 1:
  #######  SOUND TO START EXERCISE
            wave_obj = sa.WaveObject.from_wave_file(SoundWork)
            play_obj = wave_obj.play()
            play_obj.wait_done()
   
        
        window.UnHide() #while True:
        while (TimeDown > 0):   # print('I am here')
            # --------- Read and update window --------
            if not paused:
                event, values = window.read(timeout=10)
                current_time = (time_as_int() - start_time)
                TimeDown = Work - current_time
            else:
                event, values = window.read()
            # --------- Do Button Operations --------
            if event in (None, '-Next-'):        # ALWAYS give a way out of program
                break
            if event in '-RealExit-':
                exit()
            if event == '-RESET-':
                paused_time = start_time = time_as_int()
                current_time = 0
            elif event == '-RUN-PAUSE-':
                paused = not paused
                if paused:
                    paused_time = time_as_int()
                else:
                    start_time = start_time + time_as_int() - paused_time
                # Change button's text
                window['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
                
            # --------- Display timer in window --------
            window['text'].update('{:02d}:{:02d}'.format((TimeDown // 100) // 60,
                                                                (TimeDown // 100) % 60))  
            
            window['workout'].update(WorkoutList[n])  
            window['-progressbar-'].UpdateBar(NrofWorkouts-n)
            
        window.Hide()    
           
 #######  END OF EXERCISE START OF REST
        if soundon == 1:       
            wave_obj = sa.WaveObject.from_wave_file(SoundRest)
            play_obj = wave_obj.play()
            play_obj.wait_done()
           
       ######## REST TIMER ######
        current_time, paused_time, paused = 0, 0, False
        start_time2 = time_as_int()
        
        
        window2.UnHide() 
        if n >0:    
            while (TimeDownRest > 0):   # print('I am here')
                # --------- Read and update window --------
                if not paused:
                    event, values = window2.read(timeout=10)
                    current_time = (time_as_int() - start_time2)
                    TimeDownRest = Rest - current_time
                else:
                    event, values = window2.read()
                # --------- Do Button Operations --------
                if event in (None, '-Next-'):        # ALWAYS give a way out of program
                    break
                if event in '-RealExit-':
                    exit()
                if event == '-RESET-':
                    paused_time = start_time = time_as_int()
                    current_time = 0
                elif event == '-RUN-PAUSE-':
                    paused = not paused
                    if paused:
                        paused_time = time_as_int()
                    else:
                        start_time2 = start_time2 + time_as_int() - paused_time
                    # Change button's text
                    window2['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
                    
                # --------- Display timer in window --------
                window2['text2'].update('{:02d}:{:02d}'.format((TimeDownRest // 100) // 60,
                                                                    (TimeDownRest // 100) % 60))    
    
                window2['-upnext-'].update('up next: '+ WorkoutList[n-1]) 
                window2['-progressbarRest-'].UpdateBar(NrofWorkouts-n)
        

        window2.Hide() 
                
        window2['-upnext-'].update('') 
        
    lowerProgress = lowerProgress+NrofWorkouts   
    window['-progressbargesamtWork-'].UpdateBar(lowerProgress)   
    window2['-progressbargesamt-'].UpdateBar(lowerProgress)   
    ####### GO THROUGH HYDRATE ONE TIME LESS
    if gesamt == 0:
        #break
        window.close()      
        window2.close()
        window3.close()
        sg.theme('DarkRed1')
        layoutDONE = [[sg.Text('')],
                  [sg.Text('Congrats You Finished !!!', size=(20, 1), font=('Helvetica', FontTimer),
                justification='center', key='-finished-')]]
        
        windowDONE = sg.Window('Done', layoutDONE,
                   auto_size_buttons=False,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0),
                   location=(100, 100)) 
        
        event, values = windowDONE.read(timeout=200)  

        time.sleep(5)
        
        windowDONE.close()
        
        break

        
    window3.UnHide() 
    ######## HydratTiner ######
    TimeDownHydrate = Hydrate 
    current_time, paused_time, paused = 0, 0, False
    start_time3 = time_as_int()
    
    while (TimeDownHydrate > 0):   # print('I am here')
        # --------- Read and update window --------
        if not paused:
            event, values = window3.read(timeout=10)
            current_time = (time_as_int() - start_time3)
            TimeDownHydrate = Hydrate - current_time
        else:
            event, values = window3.read()
        # --------- Do Button Operations --------
        if event in (None, '-Next-'):        # ALWAYS give a way out of program
            break
        if event in '-RealExit-':
            exit()
        if event == '-RESET-':
            paused_time = start_time = time_as_int()
            current_time = 0
        elif event == '-RUN-PAUSE-':
            paused = not paused
            if paused:
                paused_time = time_as_int()
            else:
                start_time3 = start_time3 + time_as_int() - paused_time
            # Change button's text
            window3['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
            
        # --------- Display timer in window --------
        window3['text3'].update('{:02d}:{:02d}'.format((TimeDownHydrate // 100) // 60,
                                                            (TimeDownHydrate // 100) % 60))   
    
    window3.Hide() 
           #time.sleep(1)



window.close()      
window2.close()
window3.close()

