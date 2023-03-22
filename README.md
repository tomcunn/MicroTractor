# MicroTractor
Microtractor Project

The tractor runs on an ESP-8266 microcontroller. Settings for programming are as followed:

* NodeMCU 0.9 (ESP-12 Module)
* CPU Freq: 80 Mhz
* Flash Size: 4M(3M SPIFFS)
* Upload Speed: 115200

# H-Bridge

The H-Bridge is driven off of the PWM driver chip. There is a special note that the pin D4 is used to enable the chip. This created some confusion in the past. 

![image](https://user-images.githubusercontent.com/4383135/223311314-4d0d2c5d-6709-4440-a870-d436558fd90a.png)


# PWM Driver

For testing, using the adafruit PWM driver. Download the .zip file here.

https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library




# MathWorks Support Package

When you install the mathworks support package, it changes the location of the arduino. The two locations I have listed are as followed:

* C:\Users\"username"\AppData\Local\Arduino15
* C:\Users\"username"\Documents\Arduino

You need to update the settings.path in the preferences folder.
