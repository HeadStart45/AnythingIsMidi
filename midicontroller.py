import rtmidi

PAD_ONE = 40
PAD_TWO = 38
PAD_THREE = 37
PAD_FOUR = 36

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
        midiout.open_port(1)
else:
    print("No ports found")

def generateMidiMessage(on: bool, pad: int):
    if on:
        return [0x90, pad, 112]
    else:
        return [0x80, pad, 0]

def StartPlayNote(note: int) -> None:
    midiout.send_message(generateMidiMessage(True, note))

def StopPlayNote(note: int) -> None:
    midiout.send_message(generateMidiMessage(False, note))
