#receiving data from terminal using: "echo num > mypipe"

#libs
import os
import sys
import errno

# Path to be created
FIFO = "/home/pi/Desktop/LEVIS/Camera/Both/fifoExpiraments/mypipe"

#try to make the pipe
try:
    os.mkfifo(FIFO)

#check if pipe is already made
except OSError as e:
    print ("Failed to create FIFO: ", e)

#create new list
data_list = []

#open file as read
with open(FIFO, "r") as fifo:
    print("Opening FIFO...")
    
    #fill up array with 10 nums
    while (len(data_list) < 9):
        #set data read as "data" var
        data = fifo.read()
        #if data was not empty
        if (data != ""):
            #splitting data stream and storing parsed strings in list
            data_list = list(data.split("."))
            #removing last empty bit that was sent
            data_list = data_list[:-1]
            #turning strings into ints
            int_data_list = [eval(i) for i in data_list]
            for r in range(len(int_data_list)):
                print("Received: ", int_data_list[r])
            print("list = ", int_data_list, "\n")
            
