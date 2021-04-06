import RPi.GPIO as GPIO
import time
import wolk
import os
import glob

# temp sensor ds18b20
# gas detector MQ-2

# init w1 (one wire)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

default_val = 26

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	try:
		while lines[0].strip()[-3:] != 'YES':
			time.sleep(0.2)
			lines = read_temp_raw()
		equals_pos = lines[1].find('t=')
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
	except IndexError:
		temp_c = default_val
	return temp_c

pinNr = 17
run = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinNr,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def readWolkCredentials():
	import glob, os
	import pandas
	col_list = ["Key"]
	col_list2 = ["Password"]
	os.chdir("key/")
	for file in glob.glob("*.csv"):
		df = pandas.read_csv(file, usecols=col_list)
		device_key = df["Key"]
	for file in glob.glob("*.csv"):
		df = pandas.read_csv(file, usecols=col_list2)
		device_password = df["Password"]
	return (device_key[0], device_password[0])

wolk_credentials = readWolkCredentials()
if wolk_credentials is not None:
	device = wolk.Device(key=wolk_credentials[0], password=wolk_credentials[1])
else:
	print("Error reading credentials")
	sys.exit()

try:
	wolk_device = wolk.WolkConnect(
device, host="iot-elektronika.ftn.uns.ac.rs", port=1883
)
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
	return sensor_val

while run:
	try:
		gas = GPIO_read()
		temp = read_temp()
		to_Cloud(gas, temp)
		time.sleep(1)
	except KeyboardInterrupt:
		run = False

wolk_device.disconnect()
exit()
