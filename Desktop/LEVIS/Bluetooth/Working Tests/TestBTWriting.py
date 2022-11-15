#Bluetooth test: Writing/Sending 

import serial
import os

#putting code to allow opening to serial port
#os.system("sudo rfcomm watch hci0")

#opening port 1
ser = serial.Serial("/dev/rfcomm0")
ser.isOpen()			#returns True if open

while True:
    #data that needs to be sent (type the data in the console)
    i = input()
    
    #adding a new line after each send
    s = i + "\n"

    #writing data to the other end of the port 
    #.ecode() puts data into UTF-8 which is needed 
    #to be sent through the port
    ser.write(s.encode())

#close socket when program is done
ser.close()