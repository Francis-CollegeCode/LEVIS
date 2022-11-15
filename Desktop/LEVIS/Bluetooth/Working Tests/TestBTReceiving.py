#Bluetooth test: Receiving/Reading

import serial
import os

#putting code to allow opening to serial port
#os.system("sudo rfcomm watch hci0")

#opening port 1
ser = serial.Serial("/dev/rfcomm0")
ser.isOpen()		#returns True if open

while True:
    #reading data that was sent from the other end of the port 
    d = ser.readline()
    
    #.decode() turns the data from UTF-8 to text
    s= d.decode()

    #print the decoded data to the pi's terminal
    print(s)

#close socket when program is done
ser.close()