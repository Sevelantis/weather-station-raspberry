#!/bin/bash -eux

until /usr/local/bin/docker-compose -f /home/pi/weather-station/docker-compose.yml down
do
	echo 'stopping active containers.'
	sleep 2
done

until /usr/local/bin/docker-compose -f /home/pi/weather-station/docker-compose.yml up -d
do
	echo 'starting containers...'
	sleep 2
done

# process pulsein is not letting PIN23 to free
PID=$(ps auxf | grep pulseio | grep gpiochip0 | grep 23 | awk '{print$2}')

[ ! -z $PID ] && kill $PID

echo 'waiting for influxdb. . .'
sleep 5 # wait for influxdb

until /usr/bin/python3 /home/pi/weather-station/entrypoint.py > /dev/null 2>&1 &
do
	echo 'trying to start collecting data.....'
	sleep 2
done
