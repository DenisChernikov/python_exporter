import re
from subprocess import Popen, PIPE, STDOUT
from prometheus_client import Gauge, Info

import commands
import paths


def status(registry):
    g1 = Gauge(
                'python_services_status',
                'OS services status',
                ['service'],
                registry=registry
                )
    for s in ['ntpd', 'oracle']:
        g1.labels(s).set(commands.check_service(s))
    for s in ['rsyslogd', 'ora_pmon_iwtm']:
        g1.labels(s).set(commands.ps_status(s))