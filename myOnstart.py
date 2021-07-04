import myProcesses as procs

if procs.process_exists('emulationstation') == True:
    procs.killTasks('emulataionstation')