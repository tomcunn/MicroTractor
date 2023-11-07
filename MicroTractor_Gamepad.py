from tkinter import *
from tkinter.ttk import *
import socket
import time

#Define the global variables, can replace these with parameter 
#passing the future
global HeadLightCommand 
HeadLightCommand = 0
global travel 
travel = 0

TCP_IP = '192.168.4.1'
TCP_PORT = 10010
BUFFER_SIZE = 3
data_to_send = bytearray(b'\xFF\xFF\xFF\x68')
TASK_RATE = 50

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((TCP_IP, TCP_PORT))
packetID = 0
travel = 0
turn_angle = 35


#Set the high beam to false
def clickedLowBeam():
	global HeadLightCommand
	HeadLightCommand = 0
	print("Low Beam Clicked")

#Set the high beam to true
def clickedHighBeam():
	global HeadLightCommand
	HeadLightCommand = 1
	print("High Beam Clicked")

#Check for the forward direction
def clickedForward():
	global travel 
	travel = 2
	print("Forward")
	
#Check for the stop direction
def clickedStop():
	global travel
	travel = 0
	print("Stop")
	
#check for the reverse direction
def clickedReverse():
	global travel
	travel = 1
	print("Reverse")
	
def turnvalue(val):
	global turn_angle
	turn_angle = int(float(val))
	
#The send data function is what outputs the data to the tractor
def SendData():
	global HeadLightCommand
	global packetID
	global travel
	#Have to register the timer again or else it only calls once, the 100
	#is the ms amount
	window.after(TASK_RATE, SendData) 
	if packetID>100:
		packetID = 0;
	packetID=packetID + 1;
	client.send((bytearray([turn_angle, HeadLightCommand, travel, 0x68])))
	print(packetID , HeadLightCommand,turn_angle)


###################MAIN##########################################
window = Tk()
window.title("MicroTractorControls")
window.geometry('350x200')

lbl = Label(window, text=str(HeadLightCommand))
lbl.grid(column=0, row=0)

rad1 = Radiobutton(window,text='Low Beam ', value=1 ,command = clickedLowBeam)
rad2 = Radiobutton(window,text='High Beam', value=2 ,command = clickedHighBeam)
rad1.grid(column=0, row=1)
rad2.grid(column=0, row=2)
but1 = Button(window, text='forward',command = clickedForward)
but1.grid(column=0, row = 4)
but2 = Button(window, text='reverse',command =clickedReverse)
but2.grid(column=0, row = 5)
but3 = Button(window, text='stop' ,command = clickedStop)
but3.grid(column=0, row = 6)

sca1 = Scale(window,from_=35, to=55, command = turnvalue)
sca1.grid(column=0, row= 8)

window.after(TASK_RATE, SendData) 

window.mainloop()
