import subprocess

f = open('/home/pi/scripts/myControl/myConfigs/status.conf', 'w')
line = f.readline()
if line != 'reset':
    subprocess.call('emulationstation', shell=True)
f.seek(0)
f.truncate()
f.close()