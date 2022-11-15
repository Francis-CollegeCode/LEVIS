#Bluetooth test: Pressing button to send data to pi
#receive message to start code
#simulate a test case (sending data to app)

import serial
import os
import time

nums = [11,13,17,12,10,11,9]

#putting code to allow opening to serial port
#os.system("sudo rfcomm watch hci0")

#opening port 1
ser = serial.Serial("/dev/rfcomm0")

#reading data that was sent from the other end of the port 
#and decoding it     .decode() turns the data from UTF-8 to text
while True:
    #turning data to readable
    d = ser.readline()
    t = d.decode()
    q = str(t)
    s = q.strip()
    
    #if receiving the correct data from pushing the button
    if(s) == "run":

        #print the decoded data to the pi's terminal
        print("LEVIS has received your command\n")
        for n in nums:
            print(n)		#print to PI's terminal
            ser.write(str(n).encode())		#write data to app
            time.sleep(5)		#wait for 5 secs
    else:		#if something goes wrong and the wrong data gets sent
        print("wrong command, you need to send: run\n")

#close socket when program is done
ser.close()