params = {'host': '8.8.8.8',
    'cmd': '/bin/ping ',
    'param': ' -q -c 4 ',
    'interval' : 300,
    'critical' : 30,
    'logfile': '/tmp/ping.log',
    'pidfile': '/tmp/ping.pid',
    'regstring': 'rtt min/avg/max/mdev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)'
}
