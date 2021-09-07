#!/bin/bash -eux

# down
/usr/local/bin/docker-compose -f /home/pi/weather-station/docker-compose.yml down

# up
/usr/local/bin/docker-compose -f /home/pi/weather-station/docker-compose.yml up -d

sleep 3

# check influxdb connection (otherwise app fails connecting because its too fast)
host=$(docker exec -it influxdb hostname -I | awk '{print$1}')
port="8086"
while ! nc -z ${host} ${port}; do   
    echo 'waiting for influxdb..'
    sleep 1
done
echo 'INFLUXDB READY'

# process pulsein is not letting PIN23 to free
PID=$(ps auxf | grep pulseio | grep gpiochip0 | grep 23 | awk '{print$2}')
[ ! -z $PID ] && kill $PID

# kill current entrypoiny.py zombie processes
PID=$(ps auxf | grep entrypoint.py | grep python | awk '{print$2}')
[ ! -z $PID ] && kill $PID

/usr/bin/python3 /home/pi/weather-station/entrypoint.py > /home/pi/weather-station/aa 2>&1 &

ps auxf | grep entrypoint.py | grep python
