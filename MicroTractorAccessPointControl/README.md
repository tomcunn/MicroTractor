# MicroTractor Access Point Control
This software launches a microtractor as a wifi access point, and then uses a raspberrypi5 to read in the switch controller for control.

# Open Items
Hitch is too fast, need to rate limit, not sure if I do that on python side or ESP8266 side, probably python side so that I can adjust via the GUI.
Need to figure out how to rename the access point from the ESP8266 to something more cool. 

# Running Software

Make sure that you run python as "sudo" otherwise you can't access an updates from the joystick. It still shows up and everything looks good, you just don't get any stick position updates. 

The wifi on the pi needs to be set to the ESP chip


