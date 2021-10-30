#!/bin/bash -eu

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
DEBUG_MODE=false

echo "==================================================="
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
        d)
            echo "setting debug mode.."
            DEBUG_MODE=true
            ;;
    esac
done

if [[ ${IGNORE_DOCKER} = false ]]; then
    # load env vars

   source /root/.profile 

    DOCKER_COMPOSE_EXE="/home/pi/weather-station/venv/bin/docker-compose"
    # down
    $DOCKER_COMPOSE_EXE -f /home/pi/weather-station/docker-compose.yml down

    # up
    $DOCKER_COMPOSE_EXE -f /home/pi/weather-station/docker-compose.yml up -d

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
PID=$(ps auxf | grep pulseio | grep gpiochip0 | grep -w 23 | awk '{print$2}')
[ ! -z $PID ] && kill $PID

# also pin 24 
PID=$(ps auxf | grep pulseio | grep gpiochip0 | grep -w 24 | awk '{print$2}')
[ ! -z $PID ] && kill $PID

# kill current app.py zombie processes
PID=$(ps auxf | grep app.py | grep python | awk '{print$2}')
[ ! -z $PID ] && kill $PID

echo "Activating python venv.."
/home/pi/weather-station/venv/bin/activate

echo "Running app..."
PYTHON_EXE="/home/pi/weather-station/venv/bin/python3"

if [[ $DEBUG_MODE = false ]]; then
    $PYTHON_EXE /home/pi/weather-station/app.py >> /home/pi/weather-station/logs/app.log 2>&1 &
else
    $PYTHON_EXE /home/pi/weather-station/app.py
fi

ret=$?
echo "App started with code: $ret"
if [ $ret -eq 0 ]; then
    echo "____________start.sh COMPLETED_____________"
else
    echo "____________start.sh FAILED_____________"
fi
echo "==================================================="

} >> $CRON_LOGFILE 2>&1
