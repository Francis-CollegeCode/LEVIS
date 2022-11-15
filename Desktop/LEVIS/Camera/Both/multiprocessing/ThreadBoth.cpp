//libs for threading
#include <cstdlib>
#include <cstdio> 
#include <pthread.h>

using namespace std;

//function that will be called in thread
void *runRGB(void *arg){
	//cmd stuff to call the RGB Camera exe
	system("./ThreadRGB");
	
	return (void *)NULL;
}

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
    pthread_t t1, t2; //create parameter 1
    void *t1_join, *t2_join; //create parameter 2
    int t1_variable, t2_variable; //ints are like functions
	
	//needed for thread 1
	t1_variable = pthread_create(&t1, NULL, runRGB, NULL);
	if (t1_variable != 0)
		perror("pthread create failed\n");
	//needed for thread 2
	t2_variable = pthread_create(&t2, NULL, runThermal, NULL);
	if(t2_variable != 0)
		perror("pthread create failed\n");
	
	//join threads
	t1_variable = pthread_join(t1, &t1_join);
	t2_variable = pthread_join(t2, &t2_join);

	return 0;
}
