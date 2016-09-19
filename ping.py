#!/usr/bin/env python3
import subprocess
import time
import datetime
import re
import sys
import os
import atexit
import signal
from config import *
sys.path.insert(0, './PyDaemon')
from daemon3x import *


class PingDaemon(Daemon):
    def __init__(self, params):
        self.params = params
        self.pidfile = self.params['pidfile']

    def run(self):
        params = self.params
        cmd = params['cmd'] + params['param'] + params['host']
        # print(cmd)
        while True:
            # Run ping to remote host and  analyze result
            ping = self.pingcheck(cmd)
            res = self.matchres(ping)
            msg = str(int(self.timenow())) + ': '
            try:
                if float(res[2]) < self.params['critical']:
                    msg += 'Host ' + self.params['host'] + ' OK'
                else:
                    msg += 'Host ' + self.params['host'] + ' too slow (ping is: ' + res[2] + ' ms)'
            except IndexError:
                msg += 'Host ' + self.params['host'] + ' not available'
            self.logging(msg)
            # logfile = self.params['logfile']
            # try:
            #     logfile = open(logfile, 'a')
            # except FileNotFoundError:
            #     print('ERROR: Can\'t open logfile\n')
            #     sys.exit(1)
            # logfile.write(msg + '\n')
            # logfile.close()
            # print(msg)
            # Calculate time to next run, i love cron :)
            sleeptime = self.nexttime(self.timenow(), self.params['interval']) - self.timenow()
            time.sleep(sleeptime)

    def timenow(self):
        ''' Return current UTC timestamp '''
        datenow = datetime.datetime.now()
        return datenow.timestamp()

    def nexttime(self, timestamp, interval):
        ''' Return time to next run '''
        return ((timestamp + interval) // interval) * interval

    def pingcheck(self, cmd):
        ''' Run ping subprocess '''
        proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        res = proc.stdout.read()
        # proc.kill()
        return res.decode()
        # return 1

    def matchres(self, str):
        ''' function like grep '''
        match = re.compile(self.params['regstring'])
        try:
            res = match.search(str).groups()
        except AttributeError:
            res = ()
        return res

    def logging(self, msg):
        try:
            logfile = open(self.params['logfile'], 'a')
        except FileNotFoundError:
            print('ERROR: Can\'t open logfile\n')
            sys.exit(1)
        logfile.write(msg + '\n')
        logfile.close()
        return




if __name__ == '__main__':

    d = PingDaemon(params)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            d.start()
        elif 'stop' == sys.argv[1]:
            d.stop()
        elif 'restart' == sys.argv[1]:
            d.restart()
        else:
            print('Unknown command')
            sys.exit(2)
    else:
        print('Usage: ' + sys.argv[0] + ' (start|stop|restart)')
        sys.exit(2)
