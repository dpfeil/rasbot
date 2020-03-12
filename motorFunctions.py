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
  sys.stdout.write("initialize\r\n")
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
  pwm = GPIO.PWM(33, 20000)
  pwm.start(100);
  pwm2 = GPIO.PWM(18, 20000)
  pwm2.start(100);


def setForward():
  sys.stdout.write("setBackward\r\n")
  # Drive the motor clockwise
  # Motor A:
  GPIO.output(12, GPIO.HIGH) # Set AIN1
  GPIO.output(11, GPIO.LOW) # Set AIN2
  # Motor B:
  GPIO.output(15, GPIO.HIGH) # Set BIN1
  GPIO.output(16, GPIO.LOW) # Set BIN2


def setBackward():
  sys.stdout.write("setForward\r\n")
  # Drive the motor counterclockwise
  # Motor A:
  GPIO.output(12, GPIO.LOW) # Set AIN1
  GPIO.output(11, GPIO.HIGH) # Set AIN2
  # Motor B:
  GPIO.output(15, GPIO.LOW) # Set BIN1
  GPIO.output(16, GPIO.HIGH) # Set BIN2

def turnRight(speed):
  if speed == 0:
    setMotorSpeedA(90)
  setMotorSpeedB(0)
  time.sleep(0.3)
  setMotorSpeed(speed)

def turnLeft(speed):
  if speed == 0:
    setMotorSpeedB(90)
  setMotorSpeedA(0)
  time.sleep(0.3)
  setMotorSpeed(speed)


def setTurnDimeLeft():
  sys.stdout.write("setTurnDimeLeft\r\n")
  # Drive the A counterclockwise
  # Motor A:
  GPIO.output(12, GPIO.LOW) # Set AIN1
  GPIO.output(11, GPIO.HIGH) # Set AIN2
  # Drive the B clockwise
  # Motor B:
  GPIO.output(15, GPIO.HIGH) # Set BIN1
  GPIO.output(16, GPIO.LOW) # Set BIN2

def setTurnDimeRight():
  sys.stdout.write("setTurnDimeRight\r\n")
  # Drive the A clockwise
  # Motor A:
  GPIO.output(12, GPIO.HIGH) # Set AIN1
  GPIO.output(11, GPIO.LOW) # Set AIN2
  # Drive the B counterclockwise
  # Motor B:
  GPIO.output(15, GPIO.LOW) # Set BIN1
  GPIO.output(16, GPIO.HIGH) # Set BIN2


def setMotorSpeedA(percent):
  sys.stdout.write("setMotorSpeedA: " + str(percent) + "\r\n")
  global pwm
  pwm.ChangeDutyCycle(percent)

def setMotorSpeedB(percent):
  sys.stdout.write("setMotorSpeedB: " + str(percent) + "\r\n")
  global pwm2
  pwm2.ChangeDutyCycle(percent)



def setMotorSpeed(percent = 80):
  sys.stdout.write("setMotorSpeed: " + str(percent) + "\r\n")
  # Set the motor speed
  # Motor A:
  setMotorSpeedA(percent)
  #GPIO.output(33, GPIO.HIGH) # Set PWMA
  # Motor B:
  setMotorSpeedB(percent)
  #GPIO.output(18, GPIO.HIGH) # Set PWMA

def standByOff():
  sys.stdout.write("standByOff\r\n")
  # Disable STBY (standby)
  GPIO.output(13, GPIO.HIGH)

def standBy():
  sys.stdout.write("standBy\r\n")
  # Enable STBY (standby)
  GPIO.output(13, GPIO.LOW)

def move(seconds):
  print("move " + str(seconds))
  standByOff()
  time.sleep(seconds)
  standBy()


def terminate():
  sys.stdout.write("terminate\r\n")
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
speed = 0

def GetChar(Block=True):
  if Block or select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
    return sys.stdin.read(1)
  raise error('NoChar')



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
          speed += 10
          if tmpspeed == 0:
            setForward()
          setMotorSpeed(abs(speed))
        elif mc == 's' and speed != -100:
          tmpspeed = speed
          speed -= 10
          if tmpspeed == 0:
            setBackward()
          setMotorSpeed(abs(speed))
        elif mc == 'd':
          turnRight(abs(speed))
        elif mc == 'a':
	  turnLeft(abs(speed))
        elif mc == 'x':
          terminate()
          GPIO.cleanup()
          termios.tcsetattr(file_desc, termios.TCSADRAIN, old_setting)
          exit()
      except:
        pass


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


    # Reset by pressing CTRL + C
  except KeyboardInterrupt:
    sys.stdout.write("Stopped by user\r\n")
    #terminate()
    #GPIO.cleanup()
    termios.tcsetattr(file_desc, termios.TCSADRAIN, old_setting)


## Set the motor speed
## Motor A:
#GPIO.output(7, GPIO.HIGH) # Set PWMA
## Motor B:
#GPIO.output(18, GPIO.HIGH) # Set PWMB

