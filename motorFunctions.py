#!/usr/bin/env python

# Import required modules
import time
import RPi.GPIO as GPIO


def initialize():
  # Declare the GPIO settings
  GPIO.setmode(GPIO.BOARD)

  # set up GPIO pins
  GPIO.setup(7, GPIO.OUT) # Connected to PWMA
  GPIO.setup(11, GPIO.OUT) # Connected to AIN2
  GPIO.setup(12, GPIO.OUT) # Connected to AIN1
  GPIO.setup(13, GPIO.OUT) # Connected to STBY
  GPIO.setup(15, GPIO.OUT) # Connected to BIN1
  GPIO.setup(16, GPIO.OUT) # Connected to BIN2
  GPIO.setup(18, GPIO.OUT) # Connected to PWMB


def setForwad():
  # Drive the motor clockwise
  # Motor A:
  GPIO.output(12, GPIO.HIGH) # Set AIN1
  GPIO.output(11, GPIO.LOW) # Set AIN2
  # Motor B:
  GPIO.output(15, GPIO.HIGH) # Set BIN1
  GPIO.output(16, GPIO.LOW) # Set BIN2

def setBackward() {
  # Drive the motor counterclockwise
  # Motor A:
  GPIO.output(12, GPIO.LOW) # Set AIN1
  GPIO.output(11, GPIO.HIGH) # Set AIN2
  # Motor B:
  GPIO.output(15, GPIO.LOW) # Set BIN1
  GPIO.output(16, GPIO.HIGH) # Set BIN2
}


def setMotorSpeed():
  # Set the motor speed
  # Motor A:
  GPIO.output(7, GPIO.HIGH) # Set PWMA
  pwm = GPIO.PWM(7, 100)
  pwm.start(100)
  # Motor B:
  GPIO.output(18, GPIO.HIGH) # Set PWMB
  pwm2 = GPIO.PWM(18, 100)
  pwm2.start(100)

def standByOff():
  # Disable STBY (standby)
  GPIO.output(13, GPIO.HIGH)

def standBy():
  # Enable STBY (standby)
  GPIO.output(13, GPIO.LOW)

def move(seconds):
  standByOff()
  time.sleep(seconds)
  standBy()


def terminate():
  # Reset all the GPIO pins by setting them to LOW
  GPIO.output(12, GPIO.LOW) # Set AIN1
  GPIO.output(11, GPIO.LOW) # Set AIN2
  GPIO.output(7, GPIO.LOW) # Set PWMA
  GPIO.output(13, GPIO.LOW) # Set STBY
  GPIO.output(15, GPIO.LOW) # Set BIN1
  GPIO.output(16, GPIO.LOW) # Set BIN2
  GPIO.output(18, GPIO.LOW) # Set PWMB



if __name__ == '__main__':
    try:
        initialize()
        standBy()
        setMotorSpeed()
        setForward()
        move(1.9)
        time.sleep(5)
        setBackward()
        move(1.9)


        #while True:
        #    dist = distance()
        #    print ("Measured Distance = %.1f cm" % dist)
        #    time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Stopped by user")
        terminate()
        GPIO.cleanup()


## Set the motor speed
## Motor A:
#GPIO.output(7, GPIO.HIGH) # Set PWMA
## Motor B:
#GPIO.output(18, GPIO.HIGH) # Set PWMB

