#write data to fifo pipe

#libs
import os

# Path to be created
FIFO = "/home/pi/Desktop/LEVIS/Camera/Both/fifoExpiraments/mypipe"

#try to make the pipe
try:
    os.mkfifo(FIFO)

#check if pipe is already made
except OSError as e:
    print ("Failed to create FIFO: ", e)

#create new list
data_list = [101,62,73,91,21,13,39,45,54,12,42069] #42066 is how to know the c++ file can stop reading bc the pixels of the camera will only send 0-160

#open file as write
with open(FIFO, "w") as fifo:
    print("Opening FIFO...")
    #for loop that sends data in list
    for r in range(len(data_list)):
        #write num in list to pipe
        #***IMPORTANT*** Will send everything as one string unless
        #you decalre "\n". Only then will it send 10 seperate times
        fifo.write(str(data_list[r])+".")
        #print data sent
        print('Sent: ', data_list[r])
fifo.close()
            

