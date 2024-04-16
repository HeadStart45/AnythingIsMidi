
from inputController import GetDeviceList, DetectDeviceType
from midicontroller import MidiController
from utility import cls, PSGKeyGenerator
from constants import DEVICE_TYPE, GAMEPAD_KEYMAP, MOUSE_KEYMAP,  ACTION_TYPE,  OCTAVE_MODE
from constants import DEVICE_TO_KEYMAP, ACTION_TYPE_LIST, NOTES, OCTAVE_MODE_LIST
import KeyActionDirectory as kad

import PySimpleGUI as sg


# Create the controller variables
midi = MidiController()
keyGen = PSGKeyGenerator()
#deviceType = DEVICE_TYPE.NONE
# Define the elements of the GUI
portCombo = sg.Combo(midi.GetAvailablePorts(), default_value=midi.GetAvailablePorts()[0], 
                     expand_x=True, enable_events=True,
                        readonly=False, key=keyGen.PortCombo)
devicesCombo = sg.Combo(GetDeviceList(), expand_x=True, enable_events=True, readonly=False, key=keyGen.DeviceCombo)
#Set default port to midi
if(midi.GetAvailablePorts()[0] != 'NONE'):
    midi.SetPort(1)

#Note information
note = sg.InputText(' ', key='')

def GenerateLayout(keymap, text=sg.Text("Assign Keys To Notes")):
    layout = []

    for aKey in keymap:
        playNoteLayout = [[sg.Text("Note"), sg.Text(" Octave Mode"), sg.Text("   Octave")],
                          [sg.Combo(NOTES, NOTES[0], expand_x=True,enable_events=True,readonly=False,key=keyGen.Note(aKey)),
                           sg.Combo(values=OCTAVE_MODE_LIST, default_value=OCTAVE_MODE_LIST[0],
                                     expand_x=True, enable_events=True, readonly=False, key=keyGen.OctaveMode(aKey)),
                           sg.Input(default_text= '3', enable_events=True,expand_x=False, size=10, key=keyGen.Octave(aKey))]]

        layout.append([sg.Text(aKey.name), 
                       sg.Combo(values=ACTION_TYPE_LIST, default_value=ACTION_TYPE_LIST[0],
                                 expand_x=True, enable_events=True, readonly=False, key=keyGen.ActionType(aKey)),
                       sg.Frame('',layout=playNoteLayout)])
    return layout

#-Input Frames-
#Game Pad input frame
gamepadFrame = sg.Frame('', layout=[GenerateLayout(GAMEPAD_KEYMAP)],visible=False, key=keyGen.GamePadFrame)
#Mouse input frame
mouseFrame = sg.Frame('', layout=[GenerateLayout(MOUSE_KEYMAP)],visible=False, key=keyGen.MouseFrame)
#Not supported Message frame
notSupportedLayout = [[sg.Text(f'That device is not currently supported supported devices are: {[x.name for x in midi.SUPPORTED_DEVICES]}')]]
notSupportedFrame = sg.Frame('NOTE', layout=notSupportedLayout, key=keyGen.NotSupportedFrame, visible=False)
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
window = sg.Window('Anything Is MIDI', layout)

# Event loop to process user input
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel' or event == 'Quit':
        break
    if event == keyGen.PortCombo:
        if(values[keyGen.PortCombo] != 'NONE'):
            midi.SetPort(midi.available_ports.index(values[keyGen.PortCombo]))
        else:
            sg.PopupOK("No ports found. If on windows you will need to use a program like loopMidi to create a virtual port")
    if event == 'Refresh Ports':
        sg.PopupOK("Live refresh is not currently supported. You will need to close the program and relaunch")
    if event == keyGen.DeviceCombo:
        deviceType = DetectDeviceType(values[keyGen.DeviceCombo])

        window[keyGen.MouseFrame].update(visible=False)
        window[keyGen.GamePadFrame].update(visible=False)
        window[keyGen.NotSupportedFrame].update(visible=False)
        if midi.IsDeviceSupported(deviceType):
            midi.key_action_directory.AddDefaultActions(deviceType)
            midi.SetActiveInput(deviceType)
            if(midi.HasPort()):
                window['Activate'].update(disabled= False)
            else:
                sg.PopupOK("No ports found. If on windows you will need to use a program like loopMidi to create a virtual port")
            if(deviceType == DEVICE_TYPE.GAMEPAD):    
                window[keyGen.GamePadFrame].update(visible=True)
            elif(deviceType == DEVICE_TYPE.MOUSE):
                window[keyGen.MouseFrame].update(visible=True)
        else:
            window[keyGen.NotSupportedFrame].update(visible=True)
            window['Activate'].update(disabled= True)
        
        
    if event == 'Refresh Devices':
        sg.PopupOK("Live refresh is not currently supported. You will need to close the program and relaunch")
    if event == 'Activate':
        window.start_thread(lambda: SetLoop(window), ('-THREAD-', '-THEAD ENDED-'))
        sg.PopupOK("Port Activated!! You can still change the key map values!")
        window['Activate'].update(disabled= True)
        window['DeActivate'].update(disabled= False)

#Check events in frames
    if(midi.activeInputType != DEVICE_TYPE.NONE):
        for inKey in DEVICE_TO_KEYMAP[midi.activeInputType]:
            def SendPlayNote():
                if(values[keyGen.OctaveMode(inKey)] == OCTAVE_MODE.EXPLICIT.name):
                    try:
                        octave = int(values[keyGen.Octave(inKey)])
                        midi.AddPlayNoteAction(inKey, values[keyGen.Note(inKey)], octave, values[keyGen.OctaveMode(inKey)])
                    except ValueError:
                        sg.PopupOK('Invalid input in octave')
            #Check if Action Type Changed
            if event == keyGen.ActionType(inKey):
                if values[keyGen.ActionType(inKey)] == ACTION_TYPE.PLAY_NOTE.name:
                    SendPlayNote()
                if values[keyGen.ActionType(inKey)] == ACTION_TYPE.SHIFT_DOWN_FOUR.name:
                    sg.PopupOK("This action is not currently supported")
                if values[keyGen.ActionType(inKey)] == ACTION_TYPE.SHIFT_OCTAVE.name:
                    sg.PopupOK("This action is not currently supported")

            #check play note action inputs
            
                        
                else:
                    midi.AddPlayNoteAction(inKey, values[keyGen.Note(inKey)], values[keyGen.Octave(inKey)], values[keyGen.OctaveMode(inKey)])
            if event == keyGen.OctaveMode(inKey):
                if values[keyGen.OctaveMode(inKey)] == OCTAVE_MODE.EXPLICIT.name:
                    window[keyGen.Octave(inKey)].update(disabled= False, value='3')
                    values[keyGen.Octave(inKey)] = '3'
                if values[keyGen.OctaveMode(inKey)] == OCTAVE_MODE.PROGRAMMED.name:
                    window[keyGen.Octave(inKey)].update(disabled= True, value='')
                SendPlayNote()
            if event == keyGen.Octave(inKey):
                SendPlayNote()
            if event == keyGen.Note(inKey):
                SendPlayNote()

                
            
    if event == 'DeActivate':
        midi.Deactivate()
        window['Activate'].update(disabled= False)
        window['DeActivate'].update(disabled= True)
        sg.PopupOK("Port disconnected")

    

    


# Close the GUI window
window.close()


        


        
            
        




            

