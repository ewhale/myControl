import os, time, configparser
import RPi.GPIO as GPIO

gpioFan = 18

GPIO.setwarning(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpioFan, GPIO.OUT)

fan_on = False

def getCPUtemp():
    res = os.popen('vcgencmd measure_temp').readline()
    return (res.replace("temp=","").replace("'C\n",""))

def getConfig():
    config = configparser.RawConfigParser()
    configFilePath = '/home/pi/scripts/myControl/myConfigs/config.conf'
    config.read(configFilePath)
    return config

while True:
    config = getConfig()
    thresholdOn = 60
    thresholdOff = 50
    interval_value = 30
    
    try:
        thresholdOn = int(config.get('fan', 'thresholdon'))
        thresholdOff = int(config.get('fan', 'thresholdoff'))
        interval_value = float(config.get('fan', 'interval'))
    except:
        print ('Unable to access config.conf file')
        
    temp = int(float(getCPUtemp()))
    if temp >= thresholdOn:
        GPIO.output(gpioFan,1)
        fan_on = True
    else:
        if (fan_on == True & temp <= thresholdOff -5):
            GPIO.output(gpioFan,0)
            
    time.sleep(float(interval_value))