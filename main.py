import RPi.GPIO as GPIO
import time
import wolk

pinNr = 17
run = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinNr,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

device = wolk.Device(key="ywv7fn24o6alcy2l", password="b00359bb-00e7-42cf-bafc-724defe89d67")

try:
	wolk_device = wolk.WolkConnect( device=device, protocol=wolk.Protocol.JSON_SINGLE, host="iot-elektronika.ftn.uns.ac.rs", port=1883)
	wolk_device.connect()
	print("#1 Wolk Connection successful.")
except RuntimeError as e:
	print("#1 Wolk Connection unsuccessful.")
	print(str(e))
	sys.exit(-1)

def to_Cloud(info1=bool, info2=int):
	wolk_device.add_sensor_reading("Gas",info1)
	wolk_device.add_sensor_reading("Temp",info2)
	wolk_device.publish()
	print('Publishing \n\t"Gas": ' + str(info1) + '\n\t"Temp": ' + str(info2) )

def GPIO_read():
	sensor_val = bool(GPIO.input(pinNr) )
	sensor_val = not sensor_val
	print('alcohol detected: ', str(sensor_val))
	time.sleep(0.1)
	to_Cloud(sensor_val, 0)

while run:
	try:
		GPIO_read()
	except KeyboardInterrupt:
		run = False

wolk_device.disconnect()
exit()
