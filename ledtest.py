# External module imports
import RPi.GPIO as GPIO
import time

# Pin Definitons:
lsx = 26 # Broadcom pin 26 (P1 pin 37)
looptime = 100000

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(lsx, GPIO.OUT) # LED pin set as output


# Initial state for LEDs:
GPIO.output(lsx, GPIO.LOW)


#pwm.start(dc)

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        GPIO.output(lsx, GPIO.HIGH)
        count = 0
        while count < looptime:
            count = count + 1
        GPIO.output(lsx, GPIO.LOW)
        count = 0
        while count < looptime:
            count = count + 1


except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
