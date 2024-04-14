# Portfolio Project: Anything is Midi

A simple Python portfolio program for setting up nontraditional input devices as MIDI controllers

## Portfolio Notes
This program is meant as a portfolio piece for me [Liam McDonald-Lurch](https://www.linkedin.com/in/liam-mcdonald-lurch-1a965b131/). Details for setting up and using the program are below my portfolio notes. 

As well as being a functional and useful program based around an esoteric question ("Can a game controller be a MIDI pad?") this project is also made to show my ability to build straightforward, maintainable Python code.

For me, Python excels as a prototyping and internal tools development language. Putting together CLI's and simple widgets is straightforward and fast, with little boilerplate and setup overhead compared to other languages. Its excellent library of packages
and isolated virtual environments also make the encapsulation of projects easy and even fun to set up. I like to use Python if I need to take an idea to the functional stage in two days or less, since development is so speedy. These projects can easily become
internal team and developer-facing with the use of libraries like PySimpleGUI and Urwid.

One of my passions is solving development and workflow problems with code and Python is the perfect language to help solve internal problems. 

Currently a prototype/proof of concept. This 0.1 version is a one-day-build or jam using Python to turn any i/o device into a MIDI controller. 

This current version is a single implementation for a controller. On pressing the north, south, east and west buttons (X,Y,A,B on xbox) this program will send midi notes to a virtual port.

## Getting Started

### Dependencies
* [DS4](https://ds4-windows.com/) - Required if you are using a non-Windows native controller e.g. PS4, PS5 or Switch. Installing the program should be all you need to do, it will handle the controller emulation from there
* [LoopMidi](https://www.tobias-erichsen.de/software/loopmidi.html) - Required if you are on a Windows to create a virtual output port for your DAW to read. Virtual ports can be setup via IAC on Mac. [This](https://www.youtube.com/watch?v=RddfomrECPA&t=61s) youtube video shows how to do that
* Any DAW - I tested this project with the excellent free DAW [MPC Beats](https://www.akaipro.com/mpc-beats) The only requirement is the DAW can accept midi from a virtual port

### Installing

* Clone the repo.
* If on Windows: Download and install LoopMidi
* If on Mac: Setup IAC for virtual porting
* Download and install a DAW.
* Run the program
* Follow the DAW instructions for connecting to a MIDI port 

### Executing program



## Authors

Made as a portfolio piece by Liam McDonald-Lurch
[LinkedIn]https://www.linkedin.com/in/liam-mcdonald-lurch-1a965b131/

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.1
    * Initial Prototype Release

## License

This project is licensed under the Unlicense License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [music.py](https://www.youtube.com/watch?v=RddfomrECPA&t=61s)
* 
