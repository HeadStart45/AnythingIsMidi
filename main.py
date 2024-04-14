import gamepadstate as gs
import midicontroller as midi
from utility import cls


if __name__ == "__main__":
    #init the game pad
    states = gs.gamepadstate()

    while 1:
        #poll the gamepad for input
        states.PollEvents()

        #When the user presses button south send pad one play message to the output
        if states.GetButtonDown(name=gs.BUTTON_SOUTH):
            midi.StartPlayNote(midi.PAD_ONE)     

        if(states.GetButtonUp(name=gs.BUTTON_SOUTH)):
            midi.StopPlayNote(midi.PAD_ONE)


        if states.GetButtonDown(name=gs.BUTTON_WEST):
            midi.StartPlayNote(midi.PAD_TWO)

        if(states.GetButtonUp(name=gs.BUTTON_WEST)):
            midi.StopPlayNote(midi.PAD_TWO)


        if states.GetButtonDown(name=gs.BUTTON_EAST):
            midi.StartPlayNote(midi.PAD_THREE)

        if(states.GetButtonUp(name=gs.BUTTON_EAST)):
            midi.StopPlayNote(midi.PAD_THREE)


        if states.GetButtonDown(name=gs.BUTTON_NORTH):
            midi.StartPlayNote(midi.PAD_FOUR)

        if(states.GetButtonUp(name=gs.BUTTON_NORTH)):
            midi.StopPlayNote(midi.PAD_FOUR)

        


        
            
        




            

