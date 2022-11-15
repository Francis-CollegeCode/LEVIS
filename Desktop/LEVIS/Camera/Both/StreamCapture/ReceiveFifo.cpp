// C++ program to implement one side of FIFO
// This side reads 
#include <iostream>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <sstream>


using namespace std;


string convertToString(char* a, int size){
    string s = "";
    for (int i = 0; i < size; i++) {
        s = s + a[i];
    }
    return s;
}


int main()
{	
	int number;
	int xArray[5];
	int yArray[5];
	bool xy = true;
	bool fifoClose = false;
	int j = 0;
	int l = 0;
	
	string delimiter = ".";
	size_t pos = 0;
	string token;
	
    int myfile;

    // FIFO file path
    char * myfifo = "/home/pi/Desktop/LEVIS/Camera/Both/StreamCapture/mypipe";

    // Creating the named file(FIFO)
    // mkfifo(<pathname>,<permission>) 0666 means all can read
    mkfifo(myfifo, 0666);

    char message[80];
    while (!fifoClose)
    {	
	j = 0;
	l = 0;
        // First open in read only and read
        myfile = open(myfifo,O_RDONLY);
        read(myfile, message, 80);

        //Print the read string and close
        //printf("message: %s\n", message);
    
	//coverting char array into string
	int message_size = sizeof(message) / sizeof(char);
	string messageString = convertToString(message, message_size);
	//cout << "String: " + messageString << endl;

	//Parse string
	while ((pos = messageString.find(delimiter)) != std::string::npos) {
		token = messageString.substr(0, pos);
		
		//turning parsed strings into ints
		stringstream converter(token);
		converter >> number;
		//cout << "Printing int: " << number << endl;	//prints ints
		//cout << token << endl;		//prints strings
		
		if (number == 42069){			
			for(int k = 0; k < 5; k++){
				cout << "X-Array " << k << " " << xArray[k] << endl;
			}
			for(int d = 0; d < 5; d++){
				cout << "Y-Array " << d << " " << yArray[d] << endl;
			}	
			break;
		}	
		else if (number == 69420){
			close(myfile);
			cout << "closed fifo" << endl;
			fifoClose = true;
			break;
		}
		
		if (xy == true){
			xArray[j] = number;	
			xy = false;
			j++;
		}	
		else if (xy == false){
			yArray[l] = number;	
			xy = true;
			l++;
		}	
			
	    
		messageString.erase(0, pos + delimiter.length());
		
	} // end parsing strings
    } //end fifo loop
    
return 0;
} //end main


