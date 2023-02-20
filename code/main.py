import time
from prometheus_client import Gauge, start_http_server, CollectorRegistry, Info, write_to_textfile
import multiprocessing.dummy as multiprocessing

import paths
import commands
import settings
import metrics.queues as queues
import metrics.oracle as oracle
import metrics.tm as tm
import metrics.services as services


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    # start_http_server(1200)
    # Generate some requests.
    while True:
        p = multiprocessing.Pool()
        r = CollectorRegistry()
        p.map(lambda f: f(r),[queues.metrics, tm.info, tm.services, services.status])
        if settings.db_type == 'oracle':
            p.map(lambda f: f(r),[oracle.basic])
            if commands.ps_status():
                try:
                    p.map(lambda f: f(r),[oracle.alive])
                except Exception as e:
                    print(e)
        p.close()
        write_to_textfile(paths.textfile, r)
        time.sleep(15)