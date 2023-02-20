import re
import os
from subprocess import Popen, PIPE

import settings


def files_qty(path):
    return len([n for n in os.listdir(path) if os.path.isfile(os.path.join(path,n))])
    
    
def ps_status(service='ora_pmon_iwtm'):
    proc1 = Popen(['ps', '-e'], stdout=PIPE)
    proc2 = Popen(['grep', service], stdin=proc1.stdout,
                         stdout=PIPE, stderr=PIPE)
    proc1.stdout.close()
    return 1 if proc2.stdout.read().decode('utf-8').strip() else 0
    
    
def check_service(service_name):
    proc = Popen(['systemctl', 'status', service_name], stdout=PIPE)
    while True:
        line = proc.stdout.readline().decode('utf-8').strip()
        if not line:
            break
        if 'active' in line:
            return 1
    return 0
    

def check_db_files():
    proc = Popen(['/usr/lib64/nagios/plugins/mon_check_db_files.sh',
                    settings.db_type,
                    settings.schema_owner,
                    settings.password], stdout=PIPE, shell=True)
    answer = proc.stdout.read().decode('utf-8').strip()
    status = 1 if 'OK' in answer else 0
    numbers = re.findall(r'\d+', answer)
    return status, numbers
    
    
def check_alerts_oracle(path):
    proc = Popen(['/usr/lib64/nagios/plugins/mon_check_log.sh',
                    '/etc/nagios/iwmon/logpatterns/mon-alertlog-oracle.matches.patterns',
                    '/etc/nagios/iwmon/logpatterns/mon-alertlog-oracle.exclusions.patterns',
                    path], stdout=PIPE)
    answer = proc.stdout.read().decode('utf-8').strip()
    status = 1 if 'OK' in answer else 0
    return status
    
    
def check_oracle_patches():
    proc = Popen(['sudo', '-i', '-u', 'oracle',
                    '/usr/lib64/nagios/plugins/mon_check_oracle_patches.sh',
                    '/etc/nagios/iwmon/logpatterns/mon-oracle-patches.patterns'],
                    stdout=PIPE)
    answer = proc.stdout.read().decode('utf-8').strip()
    status = 1 if 'OK' in answer else 0
    numbers = re.findall(r'\d+', answer)
    return status, numbers
