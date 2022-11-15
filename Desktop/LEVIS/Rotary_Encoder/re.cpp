#include <wiringPi.h>
#include <iostream>
 
using namespace std;
long encoder;
int stateA=0;
int stateB=0;
float angle=0;
 
int wireA=23; //BCM 17
int wireB=24; //BCM 27
 
 
void A()
{
    if (stateA==stateB)
    {
        encoder++;
    }
    stateA=digitalRead(wireA);
    return;
}
 
 
void B()
{
    if (stateA==stateB)
    {
        encoder--;
    }
    stateB=digitalRead(wireB);
    return;
}
 
int main()
{
 
 
wiringPiSetup();
 
wiringPiISR(wireA, INT_EDGE_BOTH,&A);
wiringPiISR(wireB, INT_EDGE_BOTH,&B);
 
while(1)
{
angle=encoder*0.3;
cout<<"Angle is:"<<angle<<endl;
}
 
}
