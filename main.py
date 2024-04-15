
from inputController import GetDeviceList, DetectDeviceType
from midicontroller import MidiController
from utility import cls
from constants import DEVICE_TYPE, GAMEPAD_KEY, MOUSE_KEY

import PySimpleGUI as sg


# Create the controller variables
midi = MidiController()
deviceType = DEVICE_TYPE.NONE
# Define the elements of the GUI
portCombo = sg.Combo(midi.available_ports, expand_x=True, enable_events=True, readonly=False, key='-PORTCOMBO-')
devicesCombo = sg.Combo(GetDeviceList(), expand_x=True, enable_events=True, readonly=False, key='-DEVICECOMBO-')

#Game Pad inputs
gamepadLayout = [[sg.Text('Assign Game Keys To Notes')]]
for gkey in GAMEPAD_KEY:
    gamepadLayout.append([sg.Text(gkey), sg.Button('Play', key=f"-{gkey}-")])
gamepadFrame = sg.Frame('Game Pad', layout=gamepadLayout, key=('-GAMEPADFRAME-'), visible=False)

#Mouse inputs
mouseLayout = [[sg.Text('Assign Mouse Keys To Notes')]]
for mkey in MOUSE_KEY:
    mouseLayout.append([sg.Text(mkey), sg.Button('Mouse')])
mouseFrame = sg.Frame('Mouse Frame', layout=mouseLayout, key=('-MOUSEFRAME-'), visible=False)


# Define the layout of the GUI
layout = [
    [sg.Text('Choose an Output MIDI Port - (For virtual ports use loopMIDI)')],
    [portCombo, sg.Button('Refresh Ports')],
    [sg.Text('Choose an Input device type:')],
    [devicesCombo, sg.Button('Refresh Devices')],
    [gamepadFrame],[mouseFrame],
]



# Create the GUI window
window = sg.Window('My Simple App', layout)

# Event loop to process user input
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == '-PORTCOMBO-':
        midi.SetPort(midi.available_ports.index(values['-PORTCOMBO-']))
    if event == 'Refresh Ports':
        midi.RefreshPorts()
        window['-PORTCOMBO-'].update(values=midi.available_ports, value=' ')
    if event == '-DEVICECOMBO-':
        deviceType = DetectDeviceType(values["-DEVICECOMBO-"])
        window['-MOUSEFRAME-'].update(visible=False)
        window['-GAMEPADFRAME-'].update(visible=False)

        if(deviceType == DEVICE_TYPE.GAMEPAD):
            window['-GAMEPADFRAME-'].update(visible=True)
        if(deviceType == DEVICE_TYPE.MOUSE):
            window['-MOUSEFRAME-'].update(visible=True)
    if event == 'Refresh Devices':
        window['-DEVICECOMBO-'].Update(values=GetDeviceList(), value=GetDeviceList()[0])
    for gkey in GAMEPAD_KEY:
        if event == f"-{gkey}-":
            print(gkey)

    


# Close the GUI window
window.close()


        


        
            
        




            

