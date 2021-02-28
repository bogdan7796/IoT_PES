import RPi.GPIO as GPIO
import time

pinNr = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinNr,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def GPIO_read():
	global sensor_val
	global disconnect
	disconnect = False
while True:
	sensor_val = bool(GPIO.input(pinNr) )
	sensor_val = not sensor_val
	print('alcohol detected: ', str(sensor_val))
	time.sleep(0.1)

GPIO_read()
