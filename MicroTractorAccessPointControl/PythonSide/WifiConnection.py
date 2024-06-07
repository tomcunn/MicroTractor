import socket

IP_OF_COMPUTER = "192.168.4.2"

# Create a class that stores all of the parameters regarding the tractors
class ESP8266_Connection:
    def __init__(self,name):
        self.name = name
        self.address = ('192.168.4.1',5000)
        self.connection = False
    
    def register(self,data,addr):
        datatoSend =  bytes([0x00,0x00,0x00])
        if(self.connection == False):
            if(data.decode() == self.name):
                self.connection = True
                self.address = addr
                print(str(self.name) + " Connected @ " + str(self.address))
                datatoSend = bytes([0x49,0x50,0x4C])
        return datatoSend
                    

#Manage the overall UDP Interface
class UDP_Connection:
    def __init__(self):
        UDP_PORT = 5000
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((IP_OF_COMPUTER,UDP_PORT))
        self.server.setblocking(0)

    # Uses encoding
    def packetsend(self,dataToSend,connection):
        self.server.sendto(dataToSend.encode(),connection.address)

    # No encoding
    def packetsend2(self,dataToSend,addr):
        self.server.sendto(dataToSend,addr)

    # No encoding 
    def packetsend3(self,dataToSend,connection):
        self.server.sendto(dataToSend,connection.address)
