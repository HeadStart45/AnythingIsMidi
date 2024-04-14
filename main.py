import gamepadstate
import os
import rtmidi

def cls():
    os.system('cls' if os.name=='nt' else 'clear')



if __name__ == "__main__":
    states = gamepadstate()
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()

    if available_ports:
        midiout.open_port(1)
    else:
        print("No ports found")
    PAD_ONE = 40
    PAD_TWO = 38
    PAD_THREE = 37
    PAD_FOUR = 36

    pad_one_on = [0x90, 51, 112]
    pad_one_off = [0x80, 51, 0]

    def generateMidiMessage(on: bool, pad: int):
        if on:
            return [0x90, pad, 112]
        else:
            return [0x90, pad, 0]




    while 1:

        states.PollEvents()

        if states.GetButtonDown(name=BUTTON_SOUTH):
            print("Sending NoteOn event.")
            midiout.send_message(generateMidiMessage(True, PAD_ONE))
        if(states.GetButtonUp(name=BUTTON_SOUTH)):
            print("Sending NoteOff event.")
            midiout.send_message(generateMidiMessage(False, PAD_ONE))

        if states.GetButtonDown(name=BUTTON_WEST):
            print("Sending NoteOn event.")
            midiout.send_message(generateMidiMessage(True, PAD_TWO))
        if(states.GetButtonUp(name=BUTTON_WEST)):
            print("Sending NoteOff event.")
            midiout.send_message(generateMidiMessage(False, PAD_TWO))

        if states.GetButtonDown(name=BUTTON_EAST):
            print("Sending NoteOn event.")
            midiout.send_message(generateMidiMessage(True, PAD_THREE))
        if(states.GetButtonUp(name=BUTTON_EAST)):
            print("Sending NoteOff event.")
            midiout.send_message(generateMidiMessage(False, PAD_THREE))

        if states.GetButtonDown(name=BUTTON_NORTH):
            print("Sending NoteOn event.")
            midiout.send_message(generateMidiMessage(True, PAD_FOUR))
        if(states.GetButtonUp(name=BUTTON_NORTH)):
            print("Sending NoteOff event.")
            midiout.send_message(generateMidiMessage(False, PAD_FOUR))

        


        
            
        




            

