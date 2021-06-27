import psutil, os, re, subprocess

##Kill tasks
def killTasks(procnames):
    try:
        for proc in psutil.process_iter():
            if proc.name() in procnames:
                pid = str(proc.as_dict(attrs=['pid'])['pid'])
                name = proc.as_dict(attrs=['name'])['name']
                subprocess.call(['sudo', 'kill', '-15', pid])

        kodiproc = ['kodi', 'kodi.bin'] #Kodi needs SIGKILL -9 to close
        for proc in psutil.process_iter():
            if proc.name() in kodiproc:
                pid = str(proc.as_dict(attrs=['pid'])['pid'])
                name = proc.as_dict(attrs=['name'])['name']
                subprocess.call(['sudo', 'kill', '-9', pid])

    except:
        pass

##Get emulator path
def getEmulatorPath(console):
    path = 'opt/retropie/supplementary/runcommand/runcommand.sh 0 _SYS_ ' + console + ' '
    return path

##Get game path
def getGamePath(console, game):
    #Escape the spaces and brackets in game filenames
    game = game.replace(" ", "\ ")
    game = game.replace("(", "\(")
    game = game.replace(")", "\)")
    game = game.replace("'", "\\'")

    gamePath = '/home/pi/RetroPie/roms/' + console + '/' + game
    return gamePath

def processes_exists(proc_name):
    try:
        ps = subprocess.Popen('ps ax -o pid= -o args= ', shell=True, stdout=subprocess.PIPE)
        ps_pid = ps.pid
        output = ps.stdout.read()
        ps.stdout.close()
        ps.wait()
        for line in output.split('\n'):
            res = re.findall("(\d+) (.*)", line)
            if res:
                pid = int(res[0][0])
                if proc_name in res[0][1] and pid != os.getpid() and pid != ps_pid:
                    return True
        return False
    except:
        return False

def process_id(proc_name):
    try:
        ps = subprocess.Popen('ps ax -o pid= -o args= ', shell=True, stdout=subprocess.PIPE)
        ps_pid = ps.pid
        output = ps.stdout.read()
        ps.stdout.close()
        ps.wait()
        for line in output.split('\n'):
            res = re.findall("(\d+) (.*)", line)
            if res:
                pid = int(res[0][0])
                if proc_name in res[0][1] and pid != os.getpid() and pid != ps_pid:
                    return pid
        return 0
    except:
        return 0

##Run game
def runGame(console, game, source):
    print ('1')
    try:
        #Update status
        f = open('/home/pi/scripts/myControl/myConfigs/status.conf', 'rw+')
        print ('1a')
        f.seek(0)
        print ('1b')
        f.truncate()
        print ('1c')
        f.seek(0)
        print ('1d')
        f.write(source)
        print ('1e')
        f.close()
        print ('2')
        emulationstationRunning = processes_exists('emulationstation')

        procnames = ["retroarch", "ags", "uae4all2", "uae4arm", "capricerpi", "linapple", "hatari", "stella",
                    "atari800", "xroar", "vice", "daphne", "reicast", "pifba", "osmose", "gpsp", "jzintv",
                    "basiliskll", "mame", "advmame", "dgen", "openmsx", "mupen64plus", "gngeo", "dosbox", "ppsspp",
                    "simcoupe", "scummvm", "snes9x", "pisnes", "frotz", "fbzx", "fuse", "gemro", "cgenesis", "zdoom",
                    "eduke32", "lincity", "love", "alephone", "micropolis", "openbor", "openttd", "opentyrian",
                    "cannonball", "tyrquake", "ioquake3", "residualvm", "xrick", "sdlpop", "uqm", "stratagus",
                    "wolf4sdl", "solarus", "emulationstation"]

        print ('3')
        killTasks(procnames)

        print ('4')
        pid = os.fork()
        print ('5')
        if not pid:
            try:
                if ((emulationstationRunning == False and source == '') or console == ''):
                    subprocess.call('emulationstation', shell=True)
                else:
                    subprocess.call(getEmulatorPath(console) + getGamePath(console,game), shell=True)
            except:
                pass
            print ('6')
            os.exit(0)
        else:
            response = {'type':'success', 'data':'', 'message':'Successfully started game.'}
            print ('Success, game started!')
            return response
    except:
        print ('Error, failed to start game.')
        return {'type':'error', 'data':'', 'message':'Failed to start game.'}