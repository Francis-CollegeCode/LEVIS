extern "C" {
#include <wiringPi.h>
}
#include <stdio.h>


//declare vars
const int clk = 23;
const int dt = 24;
const int sw = 22;

int counter = 0;
bool clkLastState = digitalRead(clk);
bool clkState = false;
bool dtState = false;

int main(){
	printf("Started");
	wiringPiSetupGpio(); //GPIO.BCM mode
	pinMode(clk, INPUT);
	pinMode(dt, INPUT);
	pinMode(sw, INPUT);
	pullUpDnControl(clk, PUD_DOWN) ; // pulldown internal resistor
	pullUpDnControl(dt, PUD_DOWN) ; // pulldown internal resistor
	pullUpDnControl(sw, PUD_UP) ; // pullup internal resistor
	
	while(true){
		if(digitalRead(sw) == 0){
			printf("pressed");
			delay(500);
		}
		clkState = digitalRead(clk);
		dtState = digitalRead(dt);
		if(clkState != clkLastState){
			if(dtState != clkState){
				counter++;
			}
			else{
				counter--;
			}
			printf("%d",counter);
		}
		clkLastState = clkState;
		delay(10);
	}

	return 0;
}
