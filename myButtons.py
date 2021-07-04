import time, os
import RPi.GPIO as GPIO

from myNDEF import Message
from myNFC import write, read

Power =  3
Reset = 23
LED   = 14

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Power button
GPIO.setup(Power, GPIO.IN, GPIO.PUD_UP)
# Reset button
GPIO.setup(Reset, GPIO.IN, GPIO.PUD_UP)
# Status LED
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, 1)

# Functions
# Press power off: system halt (power off)
# Press power on: system resumes (power on)
# Press and release reset: Check for cart; if cart available, check if valid game in library; load if available, else restart Pi (may change to currently running emulator and/or emulation station)
# Press and hold for 2 seconds to check for cart; if cart available, write currently running game, else indicate error status with LED

def indicator(status):
    # Write triggered and success blink indicator (5 * .2 sec/blinks)
    if status == 1:
        s = 0.0
        while s != 2.0:
            GPIO.output(LED, 0)
            time.sleep(0.2)
            GPIO.output(LED, 1)
            time.sleep(0.2)
            s += 0.4
    # Error blink indicator (2 * .5 sec/blinks)
    if status == 0:
        e = 0.0
        while e != 2.0:
            GPIO.output(LED, 0)
            time.sleep(0.5)
            GPIO.output(LED, 1)
            time.sleep(0.5)
            e += 1.0

while True:
    try:
        # 'Reset' button pressed
        if GPIO.input(Reset) == True:
            timer = 0.0
            # 'Reset' timer loop; reboot or flash NFC
            while time < 2:
                if GPIO.input(Reset):
                    timer += 0.2
                    time.sleep(0.2)
                else:
                    # Status LED off
                    GPIO.output(LED, 0)
                    # Reboot
                    os.system('sudo reboot')
                        
            # 'Reset' timer > 2 secs
            if timer >= 2.0:
                try:
                    # Check for running game and write to NFC
                    indicator(1)
                    gameData = {'console':'','rom':''}
                    content = []
                    # Get current running game info
                    with open('/dev/shm/runcommand.info') as f:
                        content = f.readlines()
                    # Create record
                    filename = content[2]
                    gameData['console'] = content[0].replace('\n','')
                    gameData['rom'] = filename.rpartition('/')[2].replace('\n','')
                    
                    # Attempt to write to NFC
                    try:
                    #NEEDS A CHECK FOR VALID GAME DATA FIRST ADDED
                        # Write to NFC
                        message = Message()
                        message.addTextRecord(gameData['console'])
                        message.addTextRecord(gameData['rom'])
                        response = write(message)
                    except:
                        # Error blink status indicating no NFC is available
                        indicator(0)
                        pass
                    # Success blink status for successful write
                    indicator(1)
                    pass
                
                except:
                    # Error blink status when no game is running
                    indicator(0)
                    pass
            
        # Detect state of 'Power' and system halt if disengaged(True)
        if GPIO.input(Power) == True:
            # Call system shutdown -h
            os.system('sudo shutdown -h now')
    except:
        pass
    
    time.sleep(0.1)
