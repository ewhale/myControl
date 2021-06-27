import configparser

basePath = '/home/pi/scripts/myControl/myConfigs'
updatePath = '/home/pi/scripts/myUpdate/myControl/myConfigs'

class Config():
    @staticmethod
    def loadConfig():
        config = configparser.RawConfigParser()
        configFilePath = basePath + '/config.conf'
        config.read(configFilePath)
        return config
    
    @staticmethod
    def saveConfig(config):
        with open(basePath + '/config.conf', 'w') as configFile:
            config.write(configFile)
        return True
    
    @staticmethod
    def loadVersion():
        config = configparser.RawConfigParser()
        configFilePath = basePath + '/mycontrol.version'
        config.read(configFilePath)
        return config

    @staticmethod
    def saveVersion(config):
        with open(basePath + '/mycontrol.version', 'w') as configFile:
            config.write(configFile)
        return True

    @staticmethod
    def loadUpdateVersion():
        config = configparser.RawConfigParser()
        configFilePath = updatePath + '/mycontrol.version'
        config.read(configFilePath)
        return config