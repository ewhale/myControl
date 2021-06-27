import time, os
import RPi.GPIO as GPIO

from myNDEF import Message
from myNFC import write

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
                    # Status LED off and system reboot
                    GPIO.output(LED, 0)
                    os.system('sudo reboot')
                    
            gameData = {'console':'','rom':''}
            content = []
            try:
                # Get current running game info
                with open('/dev/shm/runcommand.info') as f:
                    content = f.readlines()
                # Create record
                filename = content[2]
                gameData['console'] = content[0].replace('\n','')
                gameData['rom'] = filename.rpartition('/')[2].replace('\n','')
            except:
                ####ADD CODE TO TRIGGER BOOT FROM CART HERE?
                pass
            
            # Blink status light to indicate NFC write attempt
            i = 0.0
            while i != 2.0:
                GPIO.output(LED, 0)
                time.sleep(0.2)
                GPIO.output(LED, 1)
                time.sleep(0.2)
                i += 0.4
                
            try:
                # Write to NFC
                message = Message()
                message.addTextRecord(gameData['console'])
                message.addTextRecord(gameData['rom'])
                
                response = write(message)
                
                # Blink status light to indicate success
                i2 = 0.0
                while i2 != 2.0:
                    GPIO.output(LED, 0)
                    time.sleep(0.2)
                    GPIO.output(LED, 1)
                    time.sleep(0.2)
                    i2 += 0.4
            except:
                # Blink status light to indicate failure
                i3 = 0.0
                while i3 != 2.0:
                    GPIO.output(LED, 0)
                    time.sleep(0.5)
                    GPIO.output(LED, 1)
                    time.sleep(0.5)
                    i3 += 1.0
                pass
            
        # Detect state of 'Power' and system halt if disengaged(True)
        if GPIO.input(Power) == True:
            # Call system shutdown -h
            os.system('sudo shutdown -h now')
    except:
        pass
    
    time.sleep(0.1)