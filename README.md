# MicroTractor
Microtractor Project
![image](https://github.com/user-attachments/assets/6e703ab6-1dd0-42e9-a74c-0489b52b0ed1)

![image](https://github.com/tomcunn/MicroTractor/assets/4383135/c8d5927e-31c4-4b76-9901-1641bfc8086a)


The tractor runs on an ESP-8266 microcontroller. Settings for programming are as followed:

* NodeMCU 0.9 (ESP-12 Module)
* CPU Freq: 80 Mhz
* Flash Size: 4M(3M SPIFFS)
* Upload Speed: 115200

# H-Bridge

The H-Bridge is driven off of the PWM driver chip. There is a special note that the pin D4 is used to enable the chip. This created some confusion in the past. 

![image](https://user-images.githubusercontent.com/4383135/223311314-4d0d2c5d-6709-4440-a870-d436558fd90a.png)

![ServoImages](https://user-images.githubusercontent.com/4383135/226780564-aff2c6b9-2ebc-4bbd-89e1-5e97490a3a8e.JPG)

![Boardimage](https://user-images.githubusercontent.com/4383135/226780839-ab01bf45-9087-4a39-9b05-800aae6f06a6.JPG)

# PWM Driver

For testing, using the adafruit PWM driver. Download the .zip file here.

https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library

![image](https://github.com/tomcunn/MicroTractor/assets/4383135/67ba1f7f-e321-42a7-8d62-66ad46b164ef)






# MathWorks Support Package

When you install the mathworks support package, it changes the location of the arduino. The two locations I have listed are as followed:

* C:\Users\"username"\AppData\Local\Arduino15
* C:\Users\"username"\Documents\Arduino

You need to update the settings.path in the preferences folder.
