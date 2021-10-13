#!/bin/bash -eux

function print_help () {
    echo "This script allows to start docker containers and app - automation purposes."
    echo -e "       -h print help"
    echo -e "       -r IGNORE_DOCKER=true - start without resetting docker"
}

function get_pod_ip()
{
    pod_name=$1
    echo $(/usr/bin/docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${pod_name})
}

function is_influxdb_visible()
{
    host=$1
    port=$2
    nc -z "${host}" "${port}"
    ret=$?
    if [ $ret -eq 0 ]; then
        echo 0
    else
        echo 1
    fi
}
CRON_LOGFILE="/var/log/mycron.log"
{
IGNORE_DOCKER=false

echo "_________"$(date)"___________"

while getopts "hr" OPT; do
    case ${OPT} in
        h)
            print_help
            exit 0
            ;;
        r)
            echo "Ignoring Docker.."
            IGNORE_DOCKER=true
            ;;    
    esac
done

if [[ ${IGNORE_DOCKER} = false ]]; then
    # down
    /usr/local/bin/docker-compose -f /home/pi/weather-station/docker-compose.yml down

    # up
    /usr/local/bin/docker-compose -f /home/pi/weather-station/docker-compose.yml up -d

    # get influxdb local IP
    host=$(get_pod_ip influxdb)
    while [ ! -n "${host}" ]; do
        host=$(get_pod_ip influxdb)
        echo "Waiting for pod ip.. host=$host"
        sleep 2
    done

    # wait  for influxdb until it opens a port 
    port="8086"

    while [ $(is_influxdb_visible $host $port) -ne 0 ]; do
        echo "trying host=$host, port=$port... -> waiting for influxdb.."
        sleep 2
    done
    echo $(nc -vz "${host}" "${port}")
fi

# process pulsein is not letting PIN23 to free, kill it
PID=$(ps auxf | grep pulseio | grep gpiochip0 | grep 23 | awk '{print$2}')
[ ! -z $PID ] && kill $PID

# also pin 24 
PID=$(ps auxf | grep pulseio | grep gpiochip0 | grep 24 | awk '{print$2}')
[ ! -z $PID ] && kill $PID

# kill current entrypoiny.py zombie processes
PID=$(ps auxf | grep entrypoint.py | grep python | awk '{print$2}')
[ ! -z $PID ] && kill $PID

echo "Starting app.."
/usr/bin/python3 /home/pi/weather-station/entrypoint.py >> /home/pi/weather-station/logs/app.log 2>&1 &

ret=$?
echo "App started with code: $ret"
if [ $ret -eq 0 ]; then
    echo "____________start.sh COMPLETED_____________"
else
    echo "____________start.sh FAILED_____________"
fi

} >> $CRON_LOGFILE 2>&1
