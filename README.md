# PowerGaze
[In development] PowerGaze is an experimental low-cost gaze tracking software using RGB webcam. It's goal is to provide a system allowing to use any Windows GUI with eye movements only.

### Requirements:
Current version of the demo was developed and tested with:
* Windows 10
* Python 3.7.11
* RGB webcam with resolution 1280 x 720 px or more

### How to install:
* Download and install [Python](https://www.python.org/downloads/)
* Download or clone the repository onto your computer
* Install all the required libraries listed in requirements.txt file, eg. using command `pip install -r requirements.txt`

### How to use:
To run the software, use `python demo.py` command.

Right after the app starts, a calibration screen is displayed - follow appearing dots with your gaze. After the callibration is finished, the cursor should roughly follow the direction of your gaze.

To perform a left mouse button click action, hold the cursor still in a desired spot.

Looking above the screen opens **mouse functions menu** with 6 buttons allowing you to perform:
* mouse drag
* double click
* right mouse button click
* copy
* paste
* hold scroll button

All of the functions are activated by clicking respective button by holding your gaze (cursor) on it.

Looking below the screen opens **additional functions menu** which contains buttons allowing you to:
* open magnifier
* close the magnifier (go back to default 100% sized screen)
* redo the callibration process
* exit the menu

Looking to the left of the screen opens Windows On-Screen Keyboard, and looking to the right of the screen - closes the keyboard.

To exit the software, press 'Esc' key when demo.py camera screen is opened.

### Limitations:
Current version, although functional, is for demonstration purposes only and needs further improvements in terms of precision, robustness, interactions and others. As of now, **it doesn't take into account head movement and rotation, so it's necessary to remain stationary in front of the camera** when using the software to achieve best results.

### Windows Magnifier settings:
Before using the software it is essential to set properties listed below. Otherwise the magnifier may not work properly with this software as it may not follow the cursor moved by your gaze point.
* Magnifier view > full screen view
* Magnifier follows > mouse pointer
* Keep the magnifier centered on the screen

You may also set preferable zoom amount (recommended 300% or more).

### Windows On-Screen Keyboard settings:
Since autopy invoked mouse clicks don't seem to work on Windows OSK, it's important to turn on the "Hover over keys" setting in the keyboard before using the software.
