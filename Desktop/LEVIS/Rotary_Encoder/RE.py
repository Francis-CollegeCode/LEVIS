#import libs
from RPi import GPIO
from time import sleep

#initialize pins
clk = 23
dt = 24
sw = 22

# GPIO Pin Settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#init vars
counter = 0
clkLastState = GPIO.input(clk)

try:

        while True:
                if GPIO.input(sw) == 0:
                    print("pressed")
                    sleep(.5)
                clkState = GPIO.input(clk)
                dtState = GPIO.input(dt)
                if clkState != clkLastState:
                        if dtState != clkState:
                                counter += 1
                        else:
                                counter -= 1
                        print (counter)
                clkLastState = clkState
                sleep(0.01)
finally:
        GPIO.cleanup()

