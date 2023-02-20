import os
from prometheus_client import Gauge

import commands


basename = '/opt/tm/queue/'
q_list = ['analyse', 'db', 'smtp', 'x2xr', 'bboard']
q_types = ['db', 'in', 'out']


def metrics(registry):
    g1 = Gauge(
            'python_queue_sizes',
            'TM queues sizes',
            ['queue_name'],
            registry=registry
        )
    g2 = Gauge(
            'python_queue_qty',
            'TM queues files total',
            ['queue_name'],
            registry=registry
        )
    for q in q_list:
        for t in q_types:
            path = os.path.join(basename, q, '.' + t)
            label = '{}/.{}'.format(q, t)
            g1.labels(label).set(os.path.getsize(path))
            g2.labels(label).set(commands.files_qty(path))