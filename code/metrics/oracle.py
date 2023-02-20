import cx_Oracle
import os
from prometheus_client import Gauge, Info
from contextlib import closing

from queries import *
import commands
import paths
import settings


def con(query):
    try:
        with closing(cx_Oracle.connect(settings.schema_owner, settings.password, 'localhost/iwtm', encoding='utf-8')) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchone()
    except cx_Oracle.DatabaseError as er:
        return er
    

def basic(registry):
    g1 = Gauge(
            'python_oracle_alive',
            'Is Oracle services alive',
            ['service'],
            registry=registry
        )
    g2 = Gauge(
            'python_oracle_all_basic',
            'Oracle Basic Info',
            ['metric', 'type'],
            registry=registry
        )
    for s in ['ora_pmon_iwtm', 'tnslsnr']:
        g1.labels(s).set(commands.ps_status(s))        
    g2.labels('oracle_alert_log', 'size').set(os.path.getsize(paths.oracle_alert_log))
    g2.labels('oracle_alerts', 'status').set(commands.check_alerts_oracle(paths.oracle_alert_log))
    g2.labels('oracle_files_qty', 'status').set(commands.check_db_files()[0])
    g2.labels('oracle_files', 'qty').set(commands.check_db_files()[1][0])
    try:
        r = con(oracle_err_count.format(minutes=30))
    except Exception as e:
        print(e)
    g2.labels('oracle_syslog_errors', 'qty').set(int(r[0]))
    g2.labels('oracle_patches', 'status').set(commands.check_oracle_patches()[0])
    

def alive(registry):
    i = Info('python_oracle_version', 'Oracle Version', registry=registry)
    g2 = Gauge(
            'python_oracle_queue_sizes',
            'Oracle queues sizes',
            ['queue_name'],
            registry=registry
        )
    g3 = Gauge(
            'python_oracle_queue_qty',
            'Oracle queues rows total',
            ['queue_name'],
            registry=registry
        )
    version = con('select * from v$version')[0]
    i.info({'version': version})
    for q in ['INDEX', 'IS', 'AGGR']:
        label = 'Oracle {}'.format(q)
        r = con(q_sum[q])[0]
        g2.labels(label).set(int(r) / 1024 if r else 0)
        r = con(q_count[q])[0]
        g3.labels(label).set(int(r) if r else 0)
