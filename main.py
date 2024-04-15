
from inputController import GetDeviceList, DetectDeviceType
from midicontroller import MidiController
from utility import cls
from constants import DEVICE_TYPE, GAMEPAD_KEYMAP, MOUSE_KEYMAP, DEVICE_TO_KEYMAP
import KeyActionDirectory as kad

import PySimpleGUI as sg


# Create the controller variables
midi = MidiController()
deviceType = DEVICE_TYPE.NONE
# Define the elements of the GUI
portCombo = sg.Combo(midi.GetAvailablePorts(), default_value=midi.GetAvailablePorts()[0], expand_x=True, enable_events=True, readonly=False, key='-PORTCOMBO-')
devicesCombo = sg.Combo(GetDeviceList(), expand_x=True, enable_events=True, readonly=False, key='-DEVICECOMBO-')
#Set default port to midi
if(midi.GetAvailablePorts()[0] != 'NONE'):
    midi.SetPort(1)

#Note information
note = sg.InputText(' ', key='')

#Game Pad inputs
gamepadLayout = [[sg.Text('Assign Game Keys To Notes')]]
for gkey in GAMEPAD_KEYMAP:
    gamepadLayout.append([sg.Text(gkey), sg.Input('60',enable_events=True, expand_x=True, key=f"-{gkey}-")])
gamepadFrame = sg.Frame('Game Pad Key Map', layout=gamepadLayout, key=('-GAMEPADFRAME-'), visible=False)

#Mouse inputs
mouseLayout = [[sg.Text('Assign Mouse Keys To Notes')]]
for mkey in MOUSE_KEYMAP:
    mouseLayout.append([sg.Text(mkey), sg.Input('60',enable_events=True, expand_x= True, key=f"-{mkey}-")])
mouseFrame = sg.Frame('Mouse Key Map', layout=mouseLayout, key=('-MOUSEFRAME-'), visible=False)

#Not supported Message
notSupportedLayout = [[sg.Text(f'That device is not currently supported supported devices are: {midi.SUPPORTED_DEVICES}')]]
notSupportedFrame = sg.Frame('NOTE', layout=notSupportedLayout, key=('-NOTSUPPORTED-'), visible=False)
# Define the layout of the GUI
layout = [
    [sg.Text('Output MIDI Port')],
    [portCombo, sg.Button('Refresh Ports')],
    [sg.Text('Input Device')],
    [devicesCombo, sg.Button('Refresh Devices')],
    [gamepadFrame],[mouseFrame],[notSupportedFrame],
    [sg.Button('Activate', disabled=True), sg.Button('DeActivate', disabled=True), sg.Button('Quit')]
]

def SetLoop(window):
    midi.ControllerLoop()

        

# Create the GUI window
window = sg.Window('My Simple App', layout)

# Event loop to process user input
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel' or event == 'Quit':
        break
    if event == '-PORTCOMBO-':
        if(values['-PORTCOMBO-'] != 'NONE'):
            midi.SetPort(midi.available_ports.index(values['-PORTCOMBO-']))
        else:
            sg.PopupOK("No ports found. If on windows you will need to use a program like loopMidi to create a virtual port")
    if event == 'Refresh Ports':
        sg.PopupOK("Live refresh is not currently supported. You will need to close the program and relaunch")
    if event == '-DEVICECOMBO-':
        deviceType = DetectDeviceType(values["-DEVICECOMBO-"])

        window['-MOUSEFRAME-'].update(visible=False)
        window['-GAMEPADFRAME-'].update(visible=False)
        window['-NOTSUPPORTED-'].update(visible=False)
        if midi.IsDeviceSupported(deviceType):
            midi.key_action_directory.AddDefaultActions(deviceType)
            midi.SetActiveInput(deviceType)
            if(midi.HasPort()):
                window['Activate'].update(disabled= False)
            else:
                sg.PopupOK("No ports found. If on windows you will need to use a program like loopMidi to create a virtual port")
            if(deviceType == DEVICE_TYPE.GAMEPAD):    
                window['-GAMEPADFRAME-'].update(visible=True)
            elif(deviceType == DEVICE_TYPE.MOUSE):
                window['-MOUSEFRAME-'].update(visible=True)
        else:
            window['-NOTSUPPORTED-'].update(visible=True)
            window['Activate'].update(disabled= True)
        
        
    if event == 'Refresh Devices':
        sg.PopupOK("Live refresh is not currently supported. You will need to close the program and relaunch")
        #window['-DEVICECOMBO-'].Update(values=GetDeviceList(), value=GetDeviceList()[0])
    if event == 'Activate':
        window.start_thread(lambda: SetLoop(window), ('-THREAD-', '-THEAD ENDED-'))
        sg.PopupOK("Port Activated!! You can still change the key map values!")
        window['Activate'].update(disabled= True)
        window['DeActivate'].update(disabled= False)

    if(midi.activeInputType != DEVICE_TYPE.NONE):
        for inKey in DEVICE_TO_KEYMAP[midi.activeInputType]:
            if event == f"-{inKey}-":
                if(values[f"-{inKey}-"] != ''):
                    midi.key_action_directory.AddPlayNoteAction(inKey, int(values[f"-{inKey}-"]))
                    print(f"Key Action Directory: {midi.key_action_directory.actionDict}")
    if event == 'DeActivate':
        midi.Deactivate()
        window['Activate'].update(disabled= False)
        window['DeActivate'].update(disabled= True)
        sg.PopupOK("Port disconnected")

    

    


# Close the GUI window
window.close()


        


        
            
        




            

