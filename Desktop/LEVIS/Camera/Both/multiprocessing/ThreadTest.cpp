#include <cstdlib>
#include <cstdio> 
#include <pthread.h>
//#include <bits/stdc++.h>


using namespace std;

void *sayHello(void *arg){
	//cout << "Hello" <<endl;
	printf("Hello \n");
	
	return (void *)NULL;
}

void *sayGoodbye(void *arg){
	//std::cout << "Goodbye" <<endl;
	printf("Goodbye \n");
	
	return (void *)NULL;
}

int main()
{
	
    // Make threads
    pthread_t t1, t2; //create parameter 1
    void *t1_join, *t2_join; //create parameter 2
    int t1_variable, t2_variable; //ints are like functions
	
	//needed for thread 1
	t1_variable = pthread_create(&t1, NULL, sayHello, NULL);
	if (t1_variable != 0)
		perror("pthread create failed\n");
	//needed for thread 2
	t2_variable = pthread_create(&t2, NULL, sayGoodbye, NULL);
	if(t2_variable != 0)
		perror("pthread create failed\n");
	
	//join threads
	t1_variable = pthread_join(t1, &t1_join);
	t2_variable = pthread_join(t2, &t2_join);

	return 0;
}

