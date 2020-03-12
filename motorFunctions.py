# Import required modules
import time
import RPi.GPIO as GPIO
import threading
import sys
import select
import tty
import termios
file_desc = sys.stdin.fileno()
old_setting = termios.tcgetattr(file_desc)
tty.setraw(sys.stdin)

def initialize():
  print("initialize")
  # Declare the GPIO settings
  GPIO.setmode(GPIO.BOARD)

  # set up GPIO pins
  GPIO.setup(33, GPIO.OUT) # Connected to PWMA
  GPIO.setup(11, GPIO.OUT) # Connected to AIN2
  GPIO.setup(12, GPIO.OUT) # Connected to AIN1
  GPIO.setup(13, GPIO.OUT) # Connected to STBY
  GPIO.setup(15, GPIO.OUT) # Connected to BIN1
  GPIO.setup(16, GPIO.OUT) # Connected to BIN2
  GPIO.setup(18, GPIO.OUT) # Connected to PWMB
  
  global pwm
  global pwm2
  pwm = GPIO.PWM(33, 2000000)
  pwm.start(100);
  pwm2 = GPIO.PWM(18, 2000000)
  pwm2.start(100);


def setBackward():
  print("setBackward")
  # Drive the motor clockwise
  # Motor A:
  GPIO.output(12, GPIO.HIGH) # Set AIN1
  GPIO.output(11, GPIO.LOW) # Set AIN2
  # Motor B:
  GPIO.output(15, GPIO.HIGH) # Set BIN1
  GPIO.output(16, GPIO.LOW) # Set BIN2


def setForward():
  print("setForward")
  # Drive the motor counterclockwise
  # Motor A:
  GPIO.output(12, GPIO.LOW) # Set AIN1
  GPIO.output(11, GPIO.HIGH) # Set AIN2
  # Motor B:
  GPIO.output(15, GPIO.LOW) # Set BIN1
  GPIO.output(16, GPIO.HIGH) # Set BIN2

def setTurnDimeLeft():
  print("setTurnDimeLeft")
  # Drive the A counterclockwise
  # Motor A:
  GPIO.output(12, GPIO.LOW) # Set AIN1
  GPIO.output(11, GPIO.HIGH) # Set AIN2
  # Drive the B clockwise
  # Motor B:
  GPIO.output(15, GPIO.HIGH) # Set BIN1
  GPIO.output(16, GPIO.LOW) # Set BIN2

def setTurnDimeRight():
  print("setTurnDimeRight")
  # Drive the A clockwise
  # Motor A:
  GPIO.output(12, GPIO.HIGH) # Set AIN1
  GPIO.output(11, GPIO.LOW) # Set AIN2
  # Drive the B counterclockwise
  # Motor B:
  GPIO.output(15, GPIO.LOW) # Set BIN1
  GPIO.output(16, GPIO.HIGH) # Set BIN2

def setMotorSpeed(percent = 80):
  print("setMotorSpeed: " + str(percent))
  # Set the motor speed
  # Motor A:
  global pwm
  #pwm = GPIO.PWM(33, 100)
  #pwm.start(100)
  pwm.ChangeDutyCycle(percent)
  #GPIO.output(33, GPIO.HIGH) # Set PWMA
  # Motor B:
  global pwm2
  #pwm2 = GPIO.PWM(18, 100)
  #pwm2.start(100)
  pwm2.ChangeDutyCycle(percent)
  #GPIO.output(18, GPIO.HIGH) # Set PWMA

def standByOff():
  print("standByOff")
  # Disable STBY (standby)
  GPIO.output(13, GPIO.HIGH)

def standBy():
  print("standBy")
  # Enable STBY (standby)
  GPIO.output(13, GPIO.LOW)

def move(seconds):
  print("move " + str(seconds))
  standByOff()
  time.sleep(seconds)
  standBy()


def terminate():
  print("terminate")
  # Reset all the GPIO pins by setting them to LOW
  global pwm
  pwm.stop()
  global pwm2
  pwm2.stop()
  GPIO.output(12, GPIO.LOW) # Set AIN1
  GPIO.output(11, GPIO.LOW) # Set AIN2
  GPIO.output(33, GPIO.LOW) # Set PWMA
  GPIO.output(13, GPIO.LOW) # Set STBY
  GPIO.output(15, GPIO.LOW) # Set BIN1
  GPIO.output(16, GPIO.LOW) # Set BIN2
  GPIO.output(18, GPIO.LOW) # Set PWMB


"""
class KeyboardThread(threading.Thread):

  def __init__(self, input_cbk = None, name='keyboard-input-thread'):
    self.input_cbk = input_cbk
    super(KeyboardThread, self).__init__(name=name)
    self.start()

  def run(self):
    while True:
      self.input_cbk(input()) #waits to get input + Return

def my_callback(inp):
  #evaluate the keyboard input
  print('You Entered: ', inp)



kthread = KeyboardThread(my_callback)
"""


pwm = None
pwm2 = None


def GetChar(Block=True):
  if Block or select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
    return sys.stdin.read(1)
  raise error('NoChar')


speed = 0

if __name__ == '__main__':
    try:
	initialize()
	setMotorSpeed(speed)
	setForward()
	standByOff()
	while True:
	  try:
	    mc = GetChar(False)
	    if mc == 'w' and speed != 100:
	      tmpspeed = speed
	      speed = speed + 10
	      if tmpspeed == 0:
                setBackward()
              setMotorSpeed(abs(speed))
	    elif mc == 's' and speed != -100:
	      tmpspeed = speed
	      speed = speed - 10
	      if tmpspeed == 0:
		setBackward()
	      setMotorSpeed(abs(speed))

	    elif mc == 'x':
	      terminate()
	      GPIO.cleanup()
              termios.tcsetattr(file_desc, termios.TCSADRAIN, old_setting)
	      exit()



	#initialize()
        #setMotorSpeed()
        #setForward()
        #move(1.9)
        #time.sleep(1)
	#setTurnDimeLeft()
	#move(1.9);
	#time.sleep(1)
        #setTurnDimeRight()
        #move(1.9);
	#time.sleep(1)
        #setBackward()
        #move(1.9)
	#terminate()
        #GPIO.cleanup()
	#termios.tcsetattr(file_desc, termios.TCSADRAIN, old_setting)

        #while True:
        #    dist = distance()
        #    print ("Measured Distance = %.1f cm" % dist)
        #    time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Stopped by user")
        #terminate()
        #GPIO.cleanup()
	termios.tcsetattr(file_desc, termios.TCSADRAIN, old_setting)


## Set the motor speed
## Motor A:
#GPIO.output(7, GPIO.HIGH) # Set PWMA
## Motor B:
#GPIO.output(18, GPIO.HIGH) # Set PWMB

