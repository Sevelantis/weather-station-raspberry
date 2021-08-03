build:
	docker-compose up -d --build && docker ps

up:
	docker-compose up -d && docker ps

down:
	docker-compose down

clean:
	docker rmi -f $(shell docker images -aq)
	docker rm -f $(shell docker ps -aq)
	docker ps -a
	docker images -a

telegraf_conf:
	docker run --rm telegraf telegraf config > telegraf/telegraf.conf
	sed -i 's/^  # urls = \["http:\/\/127\.0\.0\.1:8086"\]$$/  urls = \["http:\/\/influxdb:8086"\]/g' telegraf/telegraf.conf
	sed -i 's/^  # database = "telegraf"$$/  database = "telegraf"/' telegraf/telegraf.conf
	sed -i 's/^  # username = "telegraf"$$/  username = "telegraf"/' telegraf/telegraf.conf
	sed -i 's/^  # password = "metricsmetricsmetricsmetrics"$$/  password = "telegraf123"/' telegraf/telegraf.conf
	sed -i 's/^  hostname = ""$$/  hostname = "raspberrypi"/' telegraf/telegraf.conf

