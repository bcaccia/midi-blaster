## Description:

midi-blaster is a quick and dirty tool I wrote to help with rapidly sending MIDI commands for testing.

Right now it only outputs MIDI, although you will notice that there is an option to select a
MIDI input which is not currently implemented.

## Dependencies

The following dependencies must be installed using `pip install` for midi-blaster to run.

* pygame
* colorama

## Usage:

To launch the application:
`python midi-blaster`

1. Choose your MIDI output.
1. Select Send MIDI.
1. Enter list of MIDI to send.


Loading MIDI from a file is supported. You can type in the letter `i` which will prompt the user
with a pop up dialog to select a .txt file to load data from. 

The format of the data in the file must be:

status byte,data1,data2,send delay

See the example below:

0x90,0x36,0x00,0
0x90,0x36,0x64,0
0x90,0x36,0x7F,0

## Known Issues:

* Robust exception handling has not yet been implemented. You can crash it.
* It's difficult to get pygame to install on a Mac. If you get it installed, you'll run into crashes when attempting to load MIDI data from an external file. 
* There is no graceful way to abort sending MIDI other than to force quit the app or quit the console.