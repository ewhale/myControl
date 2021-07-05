import os, subprocess
from myNFC import read
from myProcesses import runGame

## Starts fan control
os.system('pkill -9 -f myFan.py')
subprocess.Popen('python3 /home/pi/scripts/myControl/myFan.py&', shell=True)

## Starts button control
os.system('pkill -9 -f myButtons.py')
subprocess.Popen('python3 /home/pi/scripts/myControl/myButtons.py&', shell=True)

## Check for NFC tag and boot if present
response = read()
if response.type == 'success':
    message = response.data
    runGame(message.records[0].value, message.records[1].value, 'nfc')
