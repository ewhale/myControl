import os, subprocess

## Starts fan control
os.system('pkill -9 -f myFan.py')
subprocess.Popen('python /home/pi/scripts/myControl/myFan.py&', shell=True)

## Starts button control
os.system('pkill -9 -f myButtons.py')
subprocess.Popen('python /home/pi/scripts/myControl/myButtons.py&', shell=True)