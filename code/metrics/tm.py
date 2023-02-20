import re
from subprocess import Popen, PIPE, STDOUT
from prometheus_client import Gauge, Info

import commands
import paths


def services(registry):
    g1 = Gauge(
                'python_tm_services_status_1',
                'TM services status part 1',
                ['service'],
                registry=registry
                )
    g2 = Gauge(
                'python_tm_services_status_2',
                'TM services status part 2',
                ['service'],
                registry=registry
                )
    g3 = Gauge(
                'python_tm_services_status_3',
                'TM services status part 3',
                ['service'],
                registry=registry
                )
    
    process = Popen(['/opt/tm/bin/tm', 'status'], stdout=PIPE)
    counter = 0
    while True:
        line = process.stdout.readline().decode('utf-8').strip().replace('\x1b[1m', '').replace('\x1b[0m', '')
        if not line:
            break
        pattern_label = r'(?<=iw_)\w+(?=.service)'
        pattern_state = r'(?<=service is )\w+ \(\w+\)'
        pattern_enabled = r'(?<=enabled state: ).+'
        label = re.findall(pattern_label, line)[0]
        state = re.findall(pattern_state, line)
        enabled = re.findall(pattern_enabled, line)
        def set_label(state, enabled):
            if state == ['active (running)']:
                return 1
            elif state == ['inactive (dead)'] and enabled == ['loaded (enabled)']:
                return 0
            elif state == ['inactive (dead)'] and enabled == ['masked (bad)']:
                return 2
            else:
                return 0
        if counter < 12:
            if label:
                g1.labels(label).set(set_label(state, enabled))
            else:
                print('no labels')
        elif counter < 24:
            g2.labels(label).set(set_label(state, enabled)) 
        else:
            g3.labels(label).set(set_label(state, enabled))
        counter += 1
        

def info(registry):
    i = Info('python_tm', 'Information about TM', registry=registry)
    d = {}
    for p in ['ks_mode', 'product_mode', 'version']:
        with open(paths.tm5 + p, 'r') as f:
            d[p] = f.readline().strip()
    i.info(d)