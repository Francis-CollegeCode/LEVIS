//libs for threading
#include <cstdlib>
#include <cstdio> 
#include <pthread.h>

//libs for RGB
#include<opencv2/opencv.hpp> 
#include<iostream>

//C++ things
using namespace std;
//RGB C++ things
using namespace cv;

//function that will be called in thread
void *runRGB(void *arg){
    //stuff to do in function
    Mat myImage;//Declaring a matrix to load the frames//
    namedWindow("Video Player");//Declaring the video to show the video//
    VideoCapture cap(0);//Declaring an object to capture stream of frames from default camera//
    //if (!cap.isOpened()){ //This section prompt an error message if no video stream is found//
	//	cout << "No video stream detected" << endl;
	//	system("pause");
	//	return-1;
	//}
    while (true){ //Taking an everlasting loop to show the video//
		cap >> myImage;
		if (myImage.empty()){ //Breaking the loop if no video frame is detected//
			break;
		}
		imshow("Video Player", myImage);//Showing the video//
		char c = (char)waitKey(25);//Allowing 25 milliseconds frame processing time and initiating break condition//
		if (c == 27){ //If 'Esc' is entered break the loop//
			break;
		}
    }
    cap.release();//Releasing the buffer memory
	
	return (void *)NULL;
}

//main
int main()
{
	
    // Make threads
    pthread_t t1; //create parameter 1
    void *t1_join; //create parameter 2
    int t1_variable; //ints are like functions
	
	//needed for thread
	t1_variable = pthread_create(&t1, NULL, runRGB, NULL);
	if (t1_variable != 0)
		perror("pthread create failed\n");
	
	//join threads
	t1_variable = pthread_join(t1, &t1_join);

	return 0;
}
