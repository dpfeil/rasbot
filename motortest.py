# External module imports
import RPi.GPIO as GPIO
import time

# Pin Definitons:
black = 6 # Broadcom pin 18 (P1 pin 12)
brown = 13 # Broadcom pin 23 (P1 pin 16)
orange = 16 # Broadcom pin 17 (P1 pin 11)
yellow = 19

dc = 95 # duty cycle (0-100) for PWM pin

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(black, GPIO.OUT) # LED pin set as output
GPIO.setup(brown, GPIO.OUT) # PWM pin set as output
GPIO.setup(orange, GPIO.OUT) # LED pin set as output
GPIO.setup(yellow, GPIO.OUT) # PWM pin set as output

#pwm = GPIO.PWM(pwmPin, 50)  # Initialize PWM on pwmPin 100Hz frequency
#GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up

# Initial state for LEDs:
GPIO.output(black, GPIO.LOW)
GPIO.output(brown, GPIO.LOW) # PWM pin set as output
GPIO.output(orange, GPIO.LOW) # LED pin set as output
GPIO.output(yellow, GPIO.LOW)


#pwm.start(dc)

print("Here we go! Press CTRL+C to exit")
try:
    count = 0
    while 1:
	if count == 0:
	    GPIO.output(black, GPIO.LOW)
	    GPIO.output(brown, GPIO.HIGH)
	    GPIO.output(orange, GPIO.HIGH)
	    GPIO.output(yellow, GPIO.LOW)

	if count == 1:
	    GPIO.output(black, GPIO.LOW)
            GPIO.output(brown, GPIO.HIGH)
            GPIO.output(orange, GPIO.LOW)
            GPIO.output(yellow, GPIO.HIGH)


	if count == 2:
	    GPIO.output(black, GPIO.HIGH)
            GPIO.output(brown, GPIO.LOW)
            GPIO.output(orange, GPIO.LOW)
            GPIO.output(yellow, GPIO.HIGH)


	if count == 3:
	    GPIO.output(black, GPIO.HIGH)
            GPIO.output(brown, GPIO.LOW)
            GPIO.output(orange, GPIO.HIGH)
            GPIO.output(yellow, GPIO.LOW)

	count = count + 1
	if count == 4:
	    count = 0;


except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
