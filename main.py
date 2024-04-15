
from inputController import GetDeviceList
from midicontroller import MidiController
from utility import cls

import PySimpleGUI as sg


# Create the controller variables
midi = MidiController()

# Define the elements of the GUI
portCombo = sg.Combo(midi.available_ports, expand_x=True, enable_events=True, readonly=False, key='-PORTCOMBO-')
devicesCombo = sg.Combo(GetDeviceList(), expand_x=True, enable_events=True, readonly=False, key='-DEVICECOMBO-')

# Define the layout of the GUI
layout = [
    [sg.Text('Choose an Output MIDI Port - (For virtual ports use loopMIDI)')],
    [portCombo, sg.Button('Refresh Ports')],
    [sg.Text('Choose an Input device type:')],
    [devicesCombo, sg.Button('Refresh Devices')]

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
        pass
    if event == 'Refresh Devices':
        window['-DEVICECOMBO-'].Update(values=GetDeviceList(), value=GetDeviceList()[0])

    


# Close the GUI window
window.close()


        


        
            
        




            

