#!/bin/bash
# MyControl for Retropie Installation
CURRENT=`pwd`
PARENT=`dirname $CURRENT`
SCRIPTS='/home/pi/scripts'
# Begin installation
echo "************************************************"
echo "************* Installing MyControl *************"
echo "*** A revision and modification of Pi Control **"
echo -n "************************************************"
echo -n "Warning!!! Installing the Pi Control Board on the incorrect pins on the Pi can damage your Pi!"
echo "Please use Pi Control Hardware and Software at your own risk. No will take responsibility for any damages to your Raspberry Pi that may occur, jackass."
echo "By downloading and installing our hardware and software you are agreeing to these terms."
echo "************************************************"
echo -n "Would you like to continue with the installation? (y/n): "
read REPLY
if [ $REPLY = "y" ] || [ $REPLY = "Y"]
then
    echo "********************************************"
    echo "********* Install Python 3 and pip3 ********"
    apt-get install -y python3-pip
    pip3 install --upgrade setuptools
    echo "*********** Install NFC Libraries **********"
    pip3 install RPi.GPIO
    pip3 install Adafruit-GPIO
    pip3 install Adafruit-PN532
    pip3 install psutil
    #pip3 install flask
    #pip3 install flask-api
    #pip3 install flask-httpauth
    # Copy files
    echo "****** Install MyControl Script Files ******"
    mkdir -p $SCRIPTS/myControl
    cp -r $PARENT/myControl $SCRIPTS
    chmod -R 777 $SCRIPTS
    echo "********* Enable Serial Interface **********"
    # Enable serial interface
    sed -i '\:enable_uart=0:d' /boot/config.txt
    sed -i '\:enable_uart=1:d' /boot/config.txt
    sh -c 'echo enable_uart=1 >> /boot/config.txt'
    # Update startup
    echo "********* Update Startup Commands **********"
    sed -i '\:emulationstation #auto:d' /opt/retropie/configs/all/autostart.sh
    sed -i '\:emulationstation:d' /opt/retropie/configs/all/autostart.sh
    sed -i '\:python3 /home/pi/scripts/myControl/myControl.py&:d' /opt/retropie/configs/all/autostart.sh
    sh -c 'echo python3 /home/pi/scripts/myControl/myControl.py& >> /opt/retropie/configs/all/autostart.sh'
    sh -c 'echo emulationstation >> /opt/retropie/configs/all/autostart.sh'
    rm -R /opt/retropie/configs/all/runcommand-onend.sh
    echo 'python3 /home/pi/scripts/myControl/myOnend.py&' > /opt/retropie/configs/all/runcommand-onend.sh
    chmod -R 7777 /opt/retropie/configs/all/runcommand-onend.sh
    rm -R /opt/retropie/configs/all/runcommand-onstart.sh
    echo 'python3 /home/pi/scripts/myControl/myOnstart.py&' > /opt/retropie/configs/all/runcommand-onstart.sh
    chmod -R 7777 /opt/retropie/configs/all/runcommand-onstart.sh
    echo "********** Installation Complete! **********"
    echo -n "You must reboot for changes to take effect, reboot now? (y/n): "
    read REPLY
    if [ $REPLY = "y" ] || [ $REPLY = "Y" ]
    then
        sudo reboot
    fi
fi
# End   