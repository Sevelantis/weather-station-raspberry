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

influxdb_conf:
	docker run --rm hypriot/rpi-influxdb influxd config > influxdb/influxdb.conf
	sed -i 's/^  auth-enabled = false$$/  auth-enabled = true/g' influxdb/influxdb.conf
