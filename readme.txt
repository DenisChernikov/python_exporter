1. Копируем содержимое этой директории на сервер, запускаем install.sh

2. Делаем
tm stop
reboot

3. Меняем содержимое /etc/tm/prometheus/node_exporter
на:
DAEMON_OPTS="--web.listen-address=:${PORT} --collector.textfile.directory=/opt/tm/prometheus/textfile_collector --no-collector.zfs --no-collector.hwmon --no-collector.time --no-collector.timex --no-collector.edac --no-collector.infiniband --no-collector.wifi --no-collector.entropy"

4. Reboot

5. Выполняем
systemctl restart node_exporter

6. Заходим по адресу localhost:3000 (или вместо localhost - IP)
login: admin
pass: admin
лучше сразу поменять для безопасности

слева значок "шестерёнки" -> data sources -> prometheus:
в URL пишем:
http://localhost:1111
жмём "Save & Test"

нажимаем слева сверху на "+" -> import -> Upload .json file
выбираем json из данной директории

###   PORTS
1111	prometheus
1112	node_exporter
1113	consul_exporter
1114	postgres_exporter
1115	alertmanager
1116	statsd_exporter
1117	gearman_exporter
