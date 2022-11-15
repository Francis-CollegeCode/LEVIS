#Full test: Pressing button on app to start LEVIS measurements

import serial
import os

#putting code to allow opening to serial port
#os.system("sudo rfcomm watch hci0")

#opening port 1
ser = serial.Serial("/dev/rfcomm0")

#function to convert incoming data into a readable string
def readable():
    #reading data that was sent from the other end of the port 
    #and decoding it     .decode() turns the data from UTF-8 to text
    s = ser.readline()
    t = s.decode()
    q = t.strip()
    data_readable = str(q)
    return data_readable

s = ""

while((s) != "run"):
    #store start message from app in a var
    s = readable()

    #if receiving the correct data from pushing the button
    if(s) == "run":

        #print the decoded data to the pi's terminal
        print("LEVIS has started recording data\n")
        
        #PUT LEVIS CODE HERE
        
        s = ""
        
    elif((s) == "stop"):
        print("LEVIS has paused\n")
        s = "pause"
    #else:		#if something goes wrong and the wrong data gets sent
        #print("command not understood. Received: " + str(s) + "\n")

    if (s == "pause"):
        print("Do you really want to quit?\nyes/no\n")
        decision = readable()
        
        if(decision == "yes"):
            print("LEVIS has stopped\n")
            decision = ""
            break
        elif(decision == "no"):
            print("LEVIS will continue\n")
            decision = ""
            s = ""
            
#close socket when program is done
#ser.close()