import os
from config import Config

updateDir = '/home/pi/scripts/myUpdates'
baseDir = '/home/pi/scripts/myControl'

class Settings():
    @staticmethod
    def setFanSettings(fanSettings):
        try:
            config = Config.loadConfig()
            config.set('fan', 'thresholdon', fanSettings['thresholdOn'])
            config.set('fan', 'thresholdoff', fanSettings['thresholdOff'])
            config.set('fan', 'interval', fanSettings['interval'])

            Config.saveConfig(config)
            return True
        except:
            return False

    @staticmethod
    def getFanSettings():
        try:
            config = Config.loadConfig()
            thresholdOn = int(config.get('fan', 'thresholdon'))
            thresholdOff = int(config.get('fan', 'thresholdoff'))
            interval = int(config.get('fan', 'interval'))

            return {'thresholdOn': thresholdOn, 'thresholdOff':thresholdOff, 'interval':interval}
        except:
            return {'thresholdOn':0, 'thresholdOff':0, 'interval':0}

    @staticmethod
    def setButtonSettings(option):
        try:
            config = Config.loadConfig()
            config.set('button', 'option', option['option'])

            Config.saveConfig(config)
            return True
        except:
            return False

    @staticmethod
    def getButtonSettings():
        try:
            config = Config.loadConfig()
            option = int(config.get('button', 'option'))

            return {'option':option}
        except:
            return {'option':0}

    @staticmethod
    def getVersion():
        try:
            config = Config.loadVersion()

            number = config.get('version', 'number')
            date = config.get('version', 'date')

            return {'number':number, 'date':date}
        except:
            return {'number':'1.0', 'date':''}

    @staticmethod
    def getUpdateVersion():
        try:
            config = Config.loadUpdateVersion()

            number = config.get('version', 'number')
            date = config.get('version', 'date')

            return {'number':number, 'date':date}
        except:
            return {'number':'1.0', 'date':''}

    @staticmethod
    def checkUpdates():
        response = {'update':False}
        try:
            currentVersion = Settings.getVersion()

            os.system('mkdir ' + updateDir)
            os.system('wget --no-check-certificate --content-disposition https://github.com/ewhale/myControl/raw/master/myControl.tgz')
            os.system('tar -xzf myControl.tgz myControl')
            os.system('mv ./myControl ' + updateDir + '/myControl')

            updateVersion = Settings.getUpdateVersion()

            if currentVersion['number'] != updateVersion['number']:
                response = {'update':True}

            os.system('sudo rm -R ' + updateDir)
            os.system('sudo rm -R myControl myControl.tgz')
        except:
            os.system('sudo rm -R ' + updateDir)
            os.system('sudo rm -R myControl myControl.tgz')
            response = {'update':False}

        return response

    @staticmethod
    def updateVersion():
        response = {'update':False}
        try:
            os.system('mkdir ' + updateDir)
            os.system('wget --no-check-certificate --content-disposition https://github.com/ewhale/myControl/raw/master/myControl.tgz')
            os.system('tar -xzf myControl.tgz myControl')
            os.system('mv ./myControl ' + updateDir + '/myControl')
            os.system('cp ' + baseDir + '/myConfigs/config.conf ' + updateDir + '/myControl/myConfigs/config.conf')
            print('copied config')
            os.system('sudo rm -R ' + baseDir)
            print('deleted base')
            os.system('cp -R ' + updateDir + '/myControl ' + baseDir)
            print('copied update')

            os.system('sudo rm -R ' + updateDir)
            os.system('sudo rm -R myControl myControl.tgz')
            response = {'update':Settings.getVersion()['number']}
        except:
            print('error')
            os.system('sudo rm -R ' + updateDir)
            os.system('sudo rm -R myControl myControl.tgz')
            response = {'update':False}

        return response