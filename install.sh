yum install tm-prometheus-2.3.1-7.1.1.326.x86_64.rpm tm-grafana-6.6.0-7.1.1.326.x86_64.rpm
mkdir /opt/prometheus-python-exporter
mkdir /opt/tm/share/prometheus/textfile_collector
cp -R code/* /opt/prometheus-python-exporter/
cp prometheus-python.service /usr/lib/systemd/system/

cd /opt/prometheus-python-exporter
yum install python36 python36-pip
python3.6 -m venv venv
# Переменная HTTPS_PROXY в формате
# https://user:pass@proxy.new.ru:1111 (user:pass - опционально, 1111 - порт)
# если в системе нет прокси, оставляем пустым
HTTPS_PROXY=""
activate () {
  source ./venv/bin/activate
  }
  
activate

if [ -z ${HTTPS_PROXY} ]
then
  pip install psycopg2-binary cx_Oracle prometheus_client
else
  export https_proxy=${HTTPS_PROXY}
  pip install psycopg2-binary cx_Oracle prometheus_client
fi

deactivate

systemctl daemon-reload
systemctl enable --now prometheus-python