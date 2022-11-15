//libs for threading
#include <cstdlib>
#include <cstdio> 
#include <pthread.h>

//C++ things
using namespace std;

//function that will be called in thread
void *runThermal(void *arg){
	//cmd stuff to call the Lepton Camera exe
	system("sudo sh -c 'echo performance > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor'");
	system("./raspberrypi_video -tl 3");
	
	return (void *)NULL;
}

//main
int main()
{
	
    // Make threads
    pthread_t t1; //create parameter 1
    void *t1_join; //create parameter 2
    int t1_variable; //ints are like functions
	
	//needed for thread 1
	t1_variable = pthread_create(&t1, NULL, runThermal, NULL);
	if (t1_variable != 0)
		perror("pthread create failed\n");
	
	//join threads
	t1_variable = pthread_join(t1, &t1_join);

	return 0;
}
